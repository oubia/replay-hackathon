#!/usr/bin/env python3
"""
Multimodal Knowledge Initializer

Example script showing how to ingest both text and images into the knowledge base.
"""

import base64
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from src.services.rag.service import ChromaRAGService
from src.core.config import settings

def create_sample_xray_image():
    """
    Create a simple placeholder image for demonstration.
    In production, replace this with real medical images.
    """
    # This is a 1x1 transparent PNG
    sample_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    return f"data:image/png;base64,{sample_image_base64}"

def ingest_sample_multimodal_data():
    """Ingest sample multimodal medical data"""
    
    print("Initializing Multimodal Medical Knowledge Base...")
    print(f"Using model: {settings.model_name}")
    print(f"Using vision model: {settings.vision_model}")
    print(f"Using embeddings: {settings.embedding_model}")
    print(f"Image storage: {settings.image_storage_dir}")
    print()
    
    # Initialize RAG service
    print("Creating RAG service...")
    rag_service = ChromaRAGService()
    print("✓ RAG service created")
    print()
    
    # Example 1: Text-only ingestion
    print("=" * 60)
    print("Example 1: Text-only ingestion")
    print("=" * 60)
    
    pneumonia_text = """
    # Pneumonia
    
    Pneumonia is an infection that inflames air sacs in one or both lungs.
    
    Symptoms:
    - Chest pain when breathing or coughing
    - Cough with phlegm or pus
    - Fever, sweating, and chills
    - Shortness of breath
    - Fatigue
    
    Treatment requires antibiotics and medical supervision.
    """
    
    result = rag_service.ingest_multimodal(
        text=pneumonia_text,
        source="text_only_example"
    )
    print(f"✓ Ingested {result['text_chunks']} chunks")
    print()
    
    # Example 2: Multimodal ingestion (text + image)
    print("=" * 60)
    print("Example 2: Multimodal ingestion (text + image)")
    print("=" * 60)
    print("Note: This uses a placeholder image. Replace with real X-rays.")
    print()
    
    # In production, you would load real images like this:
    # with open("chest_xray.jpg", "rb") as f:
    #     image_data = base64.b64encode(f.read()).decode()
    #     image_data = f"data:image/jpeg;base64,{image_data}"
    
    sample_image = create_sample_xray_image()
    
    xray_report = """
    Patient presents with persistent cough and fever.
    Chest X-ray ordered for evaluation of possible pneumonia.
    """
    
    result = rag_service.ingest_multimodal(
        text=xray_report,
        image_data=sample_image,
        source="multimodal_example",
        save_image=True
    )
    
    print(f"✓ Ingested {result['text_chunks']} chunks")
    if result.get('image_id'):
        print(f"✓ Stored image with ID: {result['image_id']}")
    if result.get('image_analysis'):
        print(f"✓ Image analysis generated")
        print(f"   Preview: {result['image_analysis'][:100]}...")
    print()
    
    # Example 3: Load real medical images from a directory
    print("=" * 60)
    print("Example 3: Batch ingestion from directory")
    print("=" * 60)
    
    # Check if there's a sample_data directory
    sample_dir = Path("sample_data")
    if sample_dir.exists():
        print(f"Looking for images in: {sample_dir}")
        
        image_files = list(sample_dir.glob("*.jpg")) + list(sample_dir.glob("*.png"))
        
        if image_files:
            print(f"Found {len(image_files)} images")
            
            for img_path in image_files:
                print(f"\nProcessing: {img_path.name}")
                
                # Load image
                with open(img_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()
                    image_data = f"data:image/jpeg;base64,{image_data}"
                
                # Ingest with automatic analysis
                result = rag_service.ingest_multimodal(
                    text=f"Medical image from file: {img_path.name}",
                    image_data=image_data,
                    source=f"file_{img_path.stem}",
                    save_image=True
                )
                
                if result['success']:
                    print(f"  ✓ Chunks: {result['text_chunks']}")
                    print(f"  ✓ Image ID: {result['image_id']}")
                else:
                    print(f"  ✗ Error: {result.get('error')}")
        else:
            print("No images found in sample_data directory")
    else:
        print(f"Directory {sample_dir} not found")
        print("\nTo use batch ingestion:")
        print("1. Create a 'sample_data' directory")
        print("2. Add medical images (.jpg, .png)")
        print("3. Run this script again")
    
    print()
    print("=" * 60)
    print("Knowledge base initialization complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start the backend server: python -m src.main")
    print("2. Test multimodal ingestion via API:")
    print()
    print("   import requests, base64")
    print()
    print("   # Load your medical image")
    print("   with open('xray.jpg', 'rb') as f:")
    print("       img = base64.b64encode(f.read()).decode()")
    print()
    print("   # Send to API")
    print("   response = requests.post('http://localhost:8000/ingest', json={")
    print("       'text': 'Patient with chest pain',")
    print("       'image': f'data:image/jpeg;base64,{img}',")
    print("       'source': 'my_xray'")
    print("   })")
    print()
    print("3. Use in chat:")
    print()
    print("   response = requests.post('http://localhost:8000/chat', json={")
    print("       'message': 'What do you see in this X-ray?',")
    print("       'image': f'data:image/jpeg;base64,{img}'")
    print("   })")

if __name__ == "__main__":
    try:
        ingest_sample_multimodal_data()
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
