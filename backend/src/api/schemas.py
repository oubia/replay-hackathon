from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's medical query or message")
    history: Optional[List[Dict[str, str]]] = Field(
        default=[],
        description="Chat history with role and content keys"
    )
    image: Optional[str] = Field(
        default=None,
        description="Base64 encoded image string (for future vision support)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "I have a persistent cough and mild fever for 3 days",
                "history": [
                    {"role": "user", "content": "Hello"},
                    {"role": "bot", "content": "Hi! I'm here to help with your health concerns."}
                ],
                "image": None
            }
        }

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI-generated medical guidance response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Based on your symptoms of persistent cough and mild fever..."
            }
        }

class IngestRequest(BaseModel):
    text: Optional[str] = Field(
        default=None,
        description="Medical text content to ingest into knowledge base"
    )
    image: Optional[str] = Field(
        default=None,
        description="Base64 encoded medical image (X-ray, CT scan, MRI, etc.)"
    )
    source: Optional[str] = Field(
        default="user",
        description="Source identifier for the content"
    )
    save_image: Optional[bool] = Field(
        default=True,
        description="Whether to save the image to disk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Patient presents with chest X-ray showing opacity in right lower lobe",
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
                "source": "radiology_report",
                "save_image": True
            }
        }

class IngestResponse(BaseModel):
    success: bool = Field(..., description="Whether ingestion was successful")
    text_chunks: int = Field(..., description="Number of text chunks created")
    image_id: Optional[str] = Field(None, description="ID of the stored image")
    image_analysis: Optional[str] = Field(None, description="AI analysis of the image")
    message: str = Field(..., description="Status message")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall system health status")
    rag_service: str = Field(..., description="RAG service status")
    agent_service: str = Field(..., description="Agent service status")
