"""
Image Processing Service for Medical Images

Handles image storage, analysis using OpenAI Vision API, and multimodal embeddings.
"""

import os
import base64
import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from src.core.config import settings


class ImageProcessor:
    """Process and analyze medical images"""
    
    def __init__(self):
        self.vision_model = ChatOpenAI(
            model=settings.vision_model,
            openai_api_key=settings.openai_api_key,
            max_tokens=1000
        )
        
        self.storage_dir = Path(settings.image_storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Create metadata directory
        self.metadata_dir = self.storage_dir / "metadata"
        self.metadata_dir.mkdir(exist_ok=True)
    
    def _generate_image_id(self, image_data: str) -> str:
        """Generate unique ID for image based on content hash"""
        return hashlib.sha256(image_data.encode()).hexdigest()[:16]
    
    def _save_image(self, image_data: str, image_id: str, metadata: Dict = None) -> str:
        """Save image and metadata to disk"""
        # Determine image format from data URL
        if image_data.startswith('data:'):
            header, encoded = image_data.split(',', 1)
            image_format = header.split(';')[0].split('/')[-1]
        else:
            encoded = image_data
            image_format = 'png'
        
        # Save image file
        image_path = self.storage_dir / f"{image_id}.{image_format}"
        with open(image_path, 'wb') as f:
            f.write(base64.b64decode(encoded))
        
        # Save metadata
        metadata_info = {
            'image_id': image_id,
            'format': image_format,
            'path': str(image_path),
            'created_at': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        metadata_path = self.metadata_dir / f"{image_id}.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata_info, f, indent=2)
        
        return str(image_path)
    
    def _load_image_metadata(self, image_id: str) -> Optional[Dict]:
        """Load image metadata from disk"""
        metadata_path = self.metadata_dir / f"{image_id}.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                return json.load(f)
        return None
    
    def analyze_medical_image(
        self,
        image_data: str,
        query: str = None,
        save_image: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze medical image using Vision API
        
        Args:
            image_data: Base64 encoded image or data URL
            query: Optional specific query about the image
            save_image: Whether to save the image to disk
            
        Returns:
            Dict with analysis results and image metadata
        """
        # Generate image ID
        image_id = self._generate_image_id(image_data)
        
        # Save image if requested
        image_path = None
        if save_image:
            image_path = self._save_image(image_data, image_id, {
                'query': query,
                'analyzed_at': datetime.now().isoformat()
            })
        
        # Prepare vision prompt
        if query:
            prompt = f"""You are a medical imaging assistant. Analyze this medical image and answer: {query}

Please provide:
1. Description of what you see in the image
2. Any notable medical features or findings
3. Relevant observations for medical assessment
4. Any concerns or important details

Be specific and medical in your analysis."""
        else:
            prompt = """You are a medical imaging assistant. Analyze this medical image.

Please provide:
1. Type of medical image (X-ray, CT scan, MRI, etc.)
2. Body part or area shown
3. Key findings and observations
4. Any abnormalities or areas of concern
5. Relevant medical features visible

Be specific and detailed in your medical analysis."""
        
        # Call Vision API
        try:
            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data if image_data.startswith('data:') else f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            )
            
            response = self.vision_model.invoke([message])
            analysis = response.content
            
            return {
                'image_id': image_id,
                'image_path': image_path,
                'analysis': analysis,
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'success': True
            }
            
        except Exception as e:
            return {
                'image_id': image_id,
                'image_path': image_path,
                'analysis': None,
                'error': str(e),
                'success': False
            }
    
    def generate_image_summary(self, image_data: str) -> str:
        """
        Generate a concise summary of the image for embedding
        
        Returns a text summary suitable for vector embedding
        """
        prompt = """Describe this medical image concisely in 2-3 sentences. 
Focus on: image type, body part, key findings. 
Format for text search and retrieval."""
        
        try:
            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data if image_data.startswith('data:') else f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            )
            
            response = self.vision_model.invoke([message])
            return response.content
            
        except Exception as e:
            return f"Medical image (analysis error: {str(e)})"
    
    def get_image_by_id(self, image_id: str) -> Optional[Dict]:
        """Retrieve image metadata by ID"""
        return self._load_image_metadata(image_id)
    
    def list_images(self, limit: int = 50) -> List[Dict]:
        """List all stored images with metadata"""
        images = []
        for metadata_file in sorted(self.metadata_dir.glob("*.json"), reverse=True)[:limit]:
            with open(metadata_file, 'r') as f:
                images.append(json.load(f))
        return images
    
    def delete_image(self, image_id: str) -> bool:
        """Delete image and its metadata"""
        try:
            metadata = self._load_image_metadata(image_id)
            if metadata:
                # Delete image file
                image_path = Path(metadata['path'])
                if image_path.exists():
                    image_path.unlink()
                
                # Delete metadata
                metadata_path = self.metadata_dir / f"{image_id}.json"
                if metadata_path.exists():
                    metadata_path.unlink()
                
                return True
            return False
        except Exception:
            return False


# Singleton instance
image_processor = ImageProcessor()
