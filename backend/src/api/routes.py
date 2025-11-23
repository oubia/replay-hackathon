from fastapi import APIRouter, HTTPException
from src.api.schemas import ChatRequest, ChatResponse, IngestRequest, IngestResponse, HealthResponse
from src.services.agents.service import MedicalTriageAgent
from src.services.rag.service import ChromaRAGService
from langsmith import traceable
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services (Singleton pattern)
logger.info("Initializing RAG service...")
rag_service = ChromaRAGService()
logger.info("Initializing Medical Triage Agent...")
agent_service = MedicalTriageAgent(rag_service)
logger.info("Services initialized successfully")

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "ok",
        "service": "Medical Triage System",
        "version": "1.0.0",
        "agents": ["router", "rag", "triage", "self_care", "clarification", "doctor_referral"]
    }

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test RAG service
        rag_status = "ok"
        try:
            rag_service.similarity_search("test", k=1)
        except Exception as e:
            rag_status = f"error: {str(e)}"
        
        return HealthResponse(
            status="healthy",
            rag_service=rag_status,
            agent_service="ok"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
@traceable(name="chat_endpoint")
async def chat(request: ChatRequest):
    """
    Main chat endpoint for medical triage
    
    Flow:
    1. Router Agent validates medical relevance
    2. RAG Agent searches knowledge base
    3. Triage Agent assesses risk
    4. Routes to appropriate agent (self-care, doctor referral, or clarification)
    """
    try:
        logger.info(f"Processing message: {request.message[:50]}...")
        
        response = agent_service.process_message(
            message=request.message,
            history=request.history,
            image=request.image
        )
        
        logger.info("Message processed successfully")
        return ChatResponse(response=response)
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your request: {str(e)}"
        )

@router.post("/ingest", response_model=IngestResponse)
@traceable(name="ingest_endpoint")
async def ingest(request: IngestRequest):
    """
    Ingest multimodal medical knowledge into the vector store
    
    Supports:
    - Text content (symptom descriptions, treatment guidelines, medical articles)
    - Medical images (X-rays, CT scans, MRIs, ultrasounds, etc.)
    - Combined text + image (radiology reports with images)
    
    Images are automatically analyzed using Vision AI and embedded alongside text.
    """
    try:
        if not request.text and not request.image:
            raise HTTPException(
                status_code=400,
                detail="Either text or image must be provided"
            )
        
        logger.info(f"Ingesting multimodal content from source: {request.source}")
        
        # Use multimodal ingestion
        result = rag_service.ingest_multimodal(
            text=request.text,
            image_data=request.image,
            source=request.source,
            save_image=request.save_image
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Ingestion failed: {result.get('error', 'Unknown error')}"
            )
        
        logger.info(f"Successfully ingested {result['text_chunks']} chunks")
        if result.get('image_id'):
            logger.info(f"Stored image with ID: {result['image_id']}")
        
        return IngestResponse(
            success=True,
            text_chunks=result["text_chunks"],
            image_id=result.get("image_id"),
            image_analysis=result.get("image_analysis"),
            message=f"Successfully ingested content with {result['text_chunks']} chunks"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error ingesting content: {str(e)}"
        )

@router.get("/knowledge-graph/query")
@traceable(name="kg_query_endpoint")
async def query_knowledge_graph(query: str):
    """
    Query the medical knowledge graph directly
    
    Returns relationships and entities from the graph
    """
    try:
        result = rag_service.query_knowledge_graph(query)
        return {
            "query": query,
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error querying knowledge graph: {str(e)}"
        )

@router.get("/knowledge-graph/search")
@traceable(name="hybrid_search_endpoint")
async def hybrid_search(query: str, k: int = 4):
    """
    Perform hybrid search using both vector store and knowledge graph
    
    Combines semantic search with graph relationships
    """
    try:
        results = rag_service.hybrid_search(query, k=k)
        return {
            "query": query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error performing hybrid search: {str(e)}"
        )
