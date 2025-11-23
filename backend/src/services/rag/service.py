import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import networkx as nx
from src.core.config import settings
from src.services.vision.image_processor import image_processor

class MedicalKnowledgeGraph:
    """Knowledge Graph for storing medical entities and relationships"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_entity(self, entity: str, entity_type: str, metadata: Dict = None):
        """Add a medical entity to the graph"""
        self.graph.add_node(
            entity,
            entity_type=entity_type,
            metadata=metadata or {}
        )
    
    def add_relationship(self, source: str, target: str, relation: str, metadata: Dict = None):
        """Add a relationship between entities"""
        self.graph.add_edge(
            source,
            target,
            relation=relation,
            metadata=metadata or {}
        )
    
    def get_related_entities(self, entity: str, max_hops: int = 2) -> List[Dict]:
        """Get related entities within max_hops"""
        if entity not in self.graph:
            return []
        
        related = []
        for target in nx.single_source_shortest_path_length(self.graph, entity, cutoff=max_hops):
            if target != entity:
                path_length = nx.shortest_path_length(self.graph, entity, target)
                related.append({
                    'entity': target,
                    'distance': path_length,
                    'type': self.graph.nodes[target].get('entity_type', 'unknown')
                })
        
        return related
    
    def query_graph(self, query: str) -> str:
        """Query the knowledge graph"""
        keywords = query.lower().split()
        relevant_nodes = []
        
        for node in self.graph.nodes():
            node_lower = node.lower()
            if any(keyword in node_lower for keyword in keywords):
                relevant_nodes.append(node)
        
        if not relevant_nodes:
            return "No relevant information found in knowledge graph."
        
        result = []
        for node in relevant_nodes[:5]:
            neighbors = list(self.graph.neighbors(node))
            if neighbors:
                result.append(f"{node}: related to {', '.join(neighbors[:3])}")
        
        return "\n".join(result) if result else "No relationships found."


class ChromaRAGService:
    """RAG Service with ChromaDB vector store and Knowledge Graph"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            openai_api_key=settings.openai_api_key
        )
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.Client(
            ChromaSettings(
                persist_directory=settings.chroma_persist_directory,
                anonymized_telemetry=False
            )
        )
        
        # Initialize vector store
        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name=settings.collection_name,
            embedding_function=self.embeddings,
            persist_directory=settings.chroma_persist_directory
        )
        
        # Initialize Knowledge Graph
        self.knowledge_graph = MedicalKnowledgeGraph()
        self._initialize_medical_knowledge()
        
        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def _initialize_medical_knowledge(self):
        """Initialize the knowledge graph with medical domain knowledge"""
        symptoms = [
            "fever", "cough", "headache", "fatigue", "nausea", 
            "chest pain", "shortness of breath", "dizziness", "sore throat"
        ]
        
        conditions = [
            "common cold", "flu", "pneumonia", "bronchitis", "migraine",
            "hypertension", "diabetes", "anxiety", "COVID-19"
        ]
        
        treatments = [
            "rest", "hydration", "antibiotics", "pain relievers", 
            "antiviral medication", "breathing exercises"
        ]
        
        for symptom in symptoms:
            self.knowledge_graph.add_entity(symptom, "symptom")
        
        for condition in conditions:
            self.knowledge_graph.add_entity(condition, "condition")
        
        for treatment in treatments:
            self.knowledge_graph.add_entity(treatment, "treatment")
        
        symptom_condition_map = {
            "fever": ["flu", "COVID-19", "pneumonia"],
            "cough": ["common cold", "bronchitis", "pneumonia", "COVID-19"],
            "headache": ["migraine", "flu", "hypertension"],
            "fatigue": ["flu", "COVID-19", "diabetes"],
            "chest pain": ["pneumonia", "anxiety", "hypertension"],
            "shortness of breath": ["pneumonia", "COVID-19", "anxiety"],
            "sore throat": ["common cold", "flu"],
        }
        
        for symptom, conditions_list in symptom_condition_map.items():
            for condition in conditions_list:
                self.knowledge_graph.add_relationship(
                    symptom, condition, "may_indicate"
                )
        
        condition_treatment_map = {
            "common cold": ["rest", "hydration"],
            "flu": ["rest", "hydration", "antiviral medication"],
            "pneumonia": ["antibiotics", "rest"],
            "bronchitis": ["rest", "hydration"],
            "migraine": ["pain relievers", "rest"],
            "COVID-19": ["rest", "hydration", "antiviral medication"],
        }
        
        for condition, treatments_list in condition_treatment_map.items():
            for treatment in treatments_list:
                self.knowledge_graph.add_relationship(
                    condition, treatment, "treated_with"
                )
    
    def ingest_text(self, text: str, source: str = "user") -> int:
        """Ingest text into the vector store"""
        chunks = self.text_splitter.split_text(text)
        documents = [
            Document(
                page_content=chunk,
                metadata={"source": source, "chunk_id": i}
            )
            for i, chunk in enumerate(chunks)
        ]
        self.vectorstore.add_documents(documents)
        return len(documents)
    
    def ingest_multimodal(
        self,
        text: str = None,
        image_data: str = None,
        source: str = "user",
        save_image: bool = True
    ) -> Dict[str, Any]:
        """
        Ingest multimodal content (text + image) into the vector store
        
        Args:
            text: Text content to ingest
            image_data: Base64 encoded image data
            source: Source identifier
            save_image: Whether to save image to disk
            
        Returns:
            Dict with ingestion results including image analysis
        """
        result = {
            "text_chunks": 0,
            "image_analysis": None,
            "image_id": None,
            "success": True
        }
        
        # Process image if provided
        if image_data:
            try:
                # Generate image summary for embedding
                image_summary = image_processor.generate_image_summary(image_data)
                
                # Analyze image in detail
                image_analysis = image_processor.analyze_medical_image(
                    image_data=image_data,
                    query=text if text else None,
                    save_image=save_image
                )
                
                result["image_analysis"] = image_analysis["analysis"]
                result["image_id"] = image_analysis["image_id"]
                
                # Combine text and image summary for embedding
                combined_text = ""
                if text:
                    combined_text += f"Patient Query: {text}\n\n"
                
                combined_text += f"Medical Image Analysis:\n{image_summary}\n\n"
                combined_text += f"Detailed Findings:\n{image_analysis['analysis']}"
                
                # Ingest combined content
                chunks = self.text_splitter.split_text(combined_text)
                documents = [
                    Document(
                        page_content=chunk,
                        metadata={
                            "source": source,
                            "chunk_id": i,
                            "has_image": True,
                            "image_id": image_analysis["image_id"],
                            "type": "multimodal"
                        }
                    )
                    for i, chunk in enumerate(chunks)
                ]
                self.vectorstore.add_documents(documents)
                result["text_chunks"] = len(documents)
                
            except Exception as e:
                result["success"] = False
                result["error"] = str(e)
        
        # Process text-only if no image
        elif text:
            result["text_chunks"] = self.ingest_text(text, source)
        
        return result
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search in vector store"""
        return self.vectorstore.similarity_search(query, k=k)
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """Perform similarity search with relevance scores"""
        return self.vectorstore.similarity_search_with_score(query, k=k)
    
    def get_retriever(self, k: int = 4):
        """Get a retriever for the vector store"""
        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
    
    def query_knowledge_graph(self, query: str) -> str:
        """Query the medical knowledge graph"""
        return self.knowledge_graph.query_graph(query)
    
    def hybrid_search(self, query: str, k: int = 4) -> Dict[str, Any]:
        """Perform hybrid search using both vector store and knowledge graph"""
        vector_results = self.similarity_search_with_score(query, k=k)
        graph_results = self.query_knowledge_graph(query)
        
        return {
            "vector_results": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                }
                for doc, score in vector_results
            ],
            "graph_results": graph_results
        }
