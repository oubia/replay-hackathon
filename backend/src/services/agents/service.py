from typing import Annotated, TypedDict, Literal, List, Dict, Optional
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langsmith import traceable
from src.core.config import settings
from src.services.rag.service import ChromaRAGService
from src.services.vision.image_processor import image_processor

class MedicalTriageState(TypedDict):
    """State for the medical triage system"""
    messages: Annotated[List[BaseMessage], operator.add]
    query: str
    image_data: Optional[str]  # Base64 encoded image
    image_analysis: Optional[str]  # Vision model analysis
    is_relevant: bool
    knowledge_context: str
    risk_score: int  # 0-10 scale
    risk_level: str  # "low", "medium", "high"
    recommendations: str
    needs_followup: bool
    current_agent: str


class MedicalTriageAgent:
    """
    Multi-agent medical triage system using LangGraph
    
    Agents:
    1. Router Agent - Validates query relevance
    2. RAG Agent - Searches knowledge graph
    3. Triage Agent - Analyzes risk
    4. Self-Care Agent - Provides low-risk advice
    5. Clarification Agent - Asks follow-up questions
    """
    
    def __init__(self, rag_service: ChromaRAGService):
        self.rag_service = rag_service
        
        # Initialize LLM with LangSmith tracing
        self.llm = ChatOpenAI(
            model=settings.model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            openai_api_key=settings.openai_api_key
        )
        
        # Build the workflow graph
        self.graph = self._build_graph()
    
    @traceable(name="router_agent")
    def router_agent(self, state: MedicalTriageState) -> MedicalTriageState:
        """Router Agent - Validates if query is medical-related"""
        
        system_prompt = """You are a medical query router. Your job is to determine if a user's query is related to health, medical symptoms, or wellness.
        
        Respond with ONLY 'RELEVANT' if the query is medical/health-related, or 'NOT_RELEVANT' if it's out of scope.
        
        Medical queries include:
        - Symptoms and health concerns
        - Medical conditions and diseases
        - Medications and treatments
        - Health advice and wellness
        - Medical test results
        - Medical images (X-rays, CT scans, MRIs, etc.)
        
        Out of scope:
        - General conversation
        - Non-medical topics
        - Technical support
        """
        
        query = state.get("query", "")
        image_data = state.get("image_data")
        
        # Build query context
        query_context = f"Query: {query}"
        if image_data:
            query_context += "\n[Medical image attached]"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Is this query medical-related? {query_context}")
        ]
        
        response = self.llm.invoke(messages)
        is_relevant = "RELEVANT" in response.content.upper()
        
        return {
            **state,
            "is_relevant": is_relevant,
            "current_agent": "router"
        }
    
    @traceable(name="rag_agent")
    def rag_agent(self, state: MedicalTriageState) -> MedicalTriageState:
        """RAG Agent - Searches knowledge graph and vector store, analyzes images"""
        
        query = state.get("query", "")
        image_data = state.get("image_data")
        image_analysis = None
        
        # Analyze image if provided
        if image_data:
            image_result = image_processor.analyze_medical_image(
                image_data=image_data,
                query=query,
                save_image=True
            )
            if image_result["success"]:
                image_analysis = image_result["analysis"]
        
        # Perform hybrid search (vector + knowledge graph)
        # Include image analysis in search query if available
        search_query = query
        if image_analysis:
            search_query += f"\n\nImage findings: {image_analysis[:200]}"
        
        hybrid_results = self.rag_service.hybrid_search(search_query, k=4)
        
        # Format context from vector results
        vector_context = "\n\n".join([
            f"[Source: {r['metadata'].get('source', 'unknown')}]\n{r['content']}"
            for r in hybrid_results["vector_results"]
        ])
        
        # Get knowledge graph results
        graph_context = hybrid_results["graph_results"]
        
        # Combine contexts
        knowledge_context = f"""
        === Vector Search Results ===
        {vector_context}
        
        === Knowledge Graph Results ===
        {graph_context}
        """
        
        if image_analysis:
            knowledge_context += f"""
        
        === Medical Image Analysis ===
        {image_analysis}
        """
        
        return {
            **state,
            "image_analysis": image_analysis,
            "knowledge_context": knowledge_context,
            "current_agent": "rag"
        }
    
    @traceable(name="triage_agent")
    def triage_agent(self, state: MedicalTriageState) -> MedicalTriageState:
        """Triage Agent - Analyzes symptoms and assigns risk score"""
        
        system_prompt = """You are an expert medical triage AI assistant. Analyze the patient's query and available medical knowledge to:

1. Assess the urgency/risk level (0-10 scale):
   - 0-3: Low risk (self-care appropriate)
   - 4-6: Medium risk (monitor, may need doctor)
   - 7-10: High risk (seek immediate medical attention)

2. Provide your assessment in this format:
   RISK_SCORE: [number 0-10]
   REASONING: [your analysis]
   
Consider:
- Severity of symptoms
- Duration of symptoms
- Combination of symptoms
- Red flag symptoms (chest pain, difficulty breathing, severe bleeding, etc.)
- Medical imaging findings (X-rays, CT scans, MRIs, etc.) if provided
- Visual abnormalities or concerning features in medical images
"""
        
        query = state.get("query", "")
        knowledge_context = state.get("knowledge_context", "")
        image_analysis = state.get("image_analysis")
        
        # Build comprehensive context
        context = f"""
        Patient Query: {query}
        
        Available Medical Knowledge:
        {knowledge_context}
        """
        
        if image_analysis:
            context += f"""
        
        IMPORTANT - Medical Image Analysis:
        {image_analysis}
        
        Note: The image analysis should be weighted heavily in your risk assessment.
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"{context}\n\nProvide your risk assessment.")
        ]
        
        response = self.llm.invoke(messages)
        content = response.content
        
        # Extract risk score
        risk_score = 5  # default
        try:
            for line in content.split("\n"):
                if "RISK_SCORE:" in line:
                    risk_score = int(line.split(":")[1].strip())
                    break
        except:
            pass
        
        # Determine risk level
        if risk_score <= 3:
            risk_level = "low"
        elif risk_score <= 6:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return {
            **state,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "current_agent": "triage"
        }
    
    @traceable(name="self_care_agent")
    def self_care_agent(self, state: MedicalTriageState) -> MedicalTriageState:
        """Self-Care Agent - Provides advice for low-risk conditions"""
        
        system_prompt = """You are a compassionate medical advisor for low-risk health concerns. Provide:

1. Clear explanation of the likely condition
2. Self-care recommendations
3. When to seek medical attention
4. General wellness advice

Be warm, supportive, and clear. Always include a disclaimer that this is not a substitute for professional medical advice."""
        
        query = state.get("query", "")
        knowledge_context = state.get("knowledge_context", "")
        risk_score = state.get("risk_score", 5)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
            Patient Query: {query}
            Risk Score: {risk_score}/10
            
            Medical Knowledge:
            {knowledge_context}
            
            Provide helpful self-care advice.
            """)
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "recommendations": response.content,
            "needs_followup": False,
            "current_agent": "self_care"
        }
    
    @traceable(name="clarification_agent")
    def clarification_agent(self, state: MedicalTriageState) -> MedicalTriageState:
        """Clarification Agent - Asks follow-up questions for unclear cases"""
        
        system_prompt = """You are a medical intake specialist. When information is insufficient, ask specific follow-up questions to better assess the situation.

Ask about:
- Duration and severity of symptoms
- Associated symptoms
- Medical history if relevant
- Current medications
- Recent activities or exposures

Be concise and ask 2-3 most important questions."""
        
        query = state.get("query", "")
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
            Patient Query: {query}
            
            What additional information would help assess this situation?
            """)
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "recommendations": f"I need more information to help you better:\n\n{response.content}",
            "needs_followup": True,
            "current_agent": "clarification"
        }
    
    @traceable(name="doctor_referral_agent")
    def doctor_referral_agent(self, state: MedicalTriageState) -> MedicalTriageState:
        """Doctor Referral Agent - Handles medium/high risk cases"""
        
        system_prompt = """You are a medical triage specialist for cases requiring professional medical attention.

For medium-risk cases:
- Explain why medical consultation is recommended
- Suggest timeline (within 24-48 hours)
- Provide interim care advice

For high-risk cases:
- Strongly recommend immediate medical attention
- List warning signs
- Suggest going to ER/urgent care if applicable

Always be clear but not alarmist."""
        
        query = state.get("query", "")
        knowledge_context = state.get("knowledge_context", "")
        risk_score = state.get("risk_score", 5)
        risk_level = state.get("risk_level", "medium")
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
            Patient Query: {query}
            Risk Score: {risk_score}/10 ({risk_level} risk)
            
            Medical Knowledge:
            {knowledge_context}
            
            Provide appropriate medical referral guidance.
            """)
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            **state,
            "recommendations": response.content,
            "needs_followup": False,
            "current_agent": "doctor_referral"
        }
    
    def route_after_router(self, state: MedicalTriageState) -> str:
        """Route after router agent"""
        if state.get("is_relevant", False):
            return "rag"
        else:
            return "reject"
    
    def route_after_triage(self, state: MedicalTriageState) -> str:
        """Route after triage agent based on risk level"""
        risk_level = state.get("risk_level", "medium")
        
        if risk_level == "low":
            return "self_care"
        elif risk_level in ["medium", "high"]:
            return "doctor_referral"
        else:
            return "clarification"
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        workflow = StateGraph(MedicalTriageState)
        
        # Add nodes
        workflow.add_node("router", self.router_agent)
        workflow.add_node("rag", self.rag_agent)
        workflow.add_node("triage", self.triage_agent)
        workflow.add_node("self_care", self.self_care_agent)
        workflow.add_node("clarification", self.clarification_agent)
        workflow.add_node("doctor_referral", self.doctor_referral_agent)
        
        # Add reject node
        def reject_node(state: MedicalTriageState) -> MedicalTriageState:
            return {
                **state,
                "recommendations": "I apologize, but I can only help with health and medical-related questions. Please ask a medical question, and I'll be happy to assist you.",
                "current_agent": "reject"
            }
        
        workflow.add_node("reject", reject_node)
        
        # Set entry point
        workflow.set_entry_point("router")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "router",
            self.route_after_router,
            {
                "rag": "rag",
                "reject": "reject"
            }
        )
        
        # RAG always goes to triage
        workflow.add_edge("rag", "triage")
        
        # Triage routes based on risk
        workflow.add_conditional_edges(
            "triage",
            self.route_after_triage,
            {
                "self_care": "self_care",
                "doctor_referral": "doctor_referral",
                "clarification": "clarification"
            }
        )
        
        # All terminal nodes go to END
        workflow.add_edge("self_care", END)
        workflow.add_edge("doctor_referral", END)
        workflow.add_edge("clarification", END)
        workflow.add_edge("reject", END)
        
        return workflow.compile()
    
    @traceable(name="process_message")
    def process_message(self, message: str, history: List[Dict[str, str]] = None, image: str = None) -> str:
        """Process a user message through the medical triage workflow"""
        
        # Convert history to LangChain messages
        messages = []
        if history:
            for msg in history:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant" or role == "bot":
                    messages.append(AIMessage(content=content))
        
        # Add current message
        if image:
            message_with_image = f"{message}\n\n[Medical image attached for analysis]"
            messages.append(HumanMessage(content=message_with_image))
        else:
            messages.append(HumanMessage(content=message))
        
        # Initialize state
        initial_state: MedicalTriageState = {
            "messages": messages,
            "query": message,
            "image_data": image,  # Pass image data to state
            "image_analysis": None,
            "is_relevant": False,
            "knowledge_context": "",
            "risk_score": 0,
            "risk_level": "low",
            "recommendations": "",
            "needs_followup": False,
            "current_agent": ""
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        # Return the final recommendations
        return result.get("recommendations", "I apologize, but I encountered an error processing your request.")
