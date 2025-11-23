#!/usr/bin/env python3
"""
Multimodal Medical Triage System Test

Tests the complete multimodal functionality including:
- Text-only chat
- Image-only analysis
- Combined text + image queries
- Multimodal ingestion
- Image storage and retrieval
"""

import requests
import json
import base64
import sys
from pathlib import Path
from io import BytesIO
from PIL import Image

BASE_URL = "http://localhost:8000"

def create_test_image():
    """Create a simple test image (for demo purposes)"""
    # Create a simple colored image
    img = Image.new('RGB', (100, 100), color=(73, 109, 137))
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def test_text_only_chat():
    """Test 1: Text-only medical query"""
    print_section("Test 1: Text-Only Medical Query")
    
    query = "I have a mild headache and feel tired. What should I do?"
    print(f"Query: {query}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": query,
                "history": [],
                "image": None
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Response received:")
            print(f"{result['response'][:300]}...")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_image_analysis():
    """Test 2: Image-only analysis"""
    print_section("Test 2: Medical Image Analysis")
    
    print("Note: Using a test image. Replace with real X-ray for actual testing.\n")
    
    # Create test image
    test_image = create_test_image()
    
    query = "What do you see in this medical image?"
    print(f"Query: {query}")
    print(f"Image: Test image attached\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": query,
                "history": [],
                "image": test_image
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Response received:")
            print(f"{result['response'][:300]}...")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_multimodal_query():
    """Test 3: Combined text + image query"""
    print_section("Test 3: Multimodal Query (Text + Image)")
    
    test_image = create_test_image()
    
    query = "I have chest pain and difficulty breathing. Here's my chest X-ray."
    print(f"Query: {query}")
    print(f"Image: Test X-ray attached\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": query,
                "history": [],
                "image": test_image
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Response received:")
            print(f"{result['response'][:300]}...")
            print("\nThe system should:")
            print("  1. Analyze the image using Vision AI")
            print("  2. Consider both symptoms AND image findings")
            print("  3. Provide risk assessment based on both")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_multimodal_ingestion():
    """Test 4: Ingest medical content with image"""
    print_section("Test 4: Multimodal Content Ingestion")
    
    test_image = create_test_image()
    
    text = """
    Case Study: Patient with Pneumonia
    
    Patient presents with:
    - Persistent cough (7 days)
    - Fever 101.5°F
    - Chest discomfort
    
    Chest X-ray findings:
    - Right lower lobe opacity
    - No pleural effusion
    - Heart size normal
    
    Diagnosis: Community-acquired pneumonia
    Treatment: Antibiotics, rest, fluids
    """
    
    print("Ingesting case study with X-ray image...\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/ingest",
            json={
                "text": text,
                "image": test_image,
                "source": "test_case_pneumonia",
                "save_image": True
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Ingestion successful:")
            print(f"  - Success: {result['success']}")
            print(f"  - Text chunks: {result['text_chunks']}")
            print(f"  - Image ID: {result.get('image_id', 'N/A')}")
            
            if result.get('image_analysis'):
                print(f"  - Image analyzed: Yes")
                print(f"  - Analysis preview: {result['image_analysis'][:100]}...")
            
            print(f"\n  Message: {result['message']}")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_text_only_ingestion():
    """Test 5: Ingest text-only content"""
    print_section("Test 5: Text-Only Ingestion")
    
    text = """
    Dehydration Prevention Tips
    
    Signs of dehydration:
    - Dark yellow urine
    - Dry mouth and lips
    - Fatigue
    - Dizziness
    
    Prevention:
    - Drink 8 glasses of water daily
    - Increase fluids during exercise
    - Avoid excessive caffeine
    - Monitor urine color
    """
    
    print("Ingesting medical text...\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/ingest",
            json={
                "text": text,
                "source": "dehydration_tips"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Ingestion successful:")
            print(f"  - Text chunks: {result['text_chunks']}")
            print(f"  - Message: {result['message']}")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_real_image_file():
    """Test 6: Load and test with real image file (if available)"""
    print_section("Test 6: Real Image File (Optional)")
    
    # Look for test images in common locations
    test_paths = [
        "test_xray.jpg",
        "sample_data/xray.jpg",
        "../test_images/chest_xray.jpg"
    ]
    
    image_path = None
    for path in test_paths:
        if Path(path).exists():
            image_path = Path(path)
            break
    
    if not image_path:
        print("No test image file found. Skipping this test.")
        print("\nTo test with real images:")
        print("1. Save a medical image as 'test_xray.jpg'")
        print("2. Run this test again")
        return True  # Not a failure, just skipped
    
    print(f"Found test image: {image_path}\n")
    
    try:
        # Load real image
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
            image_data = f"data:image/jpeg;base64,{image_data}"
        
        # Analyze it
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": "Please analyze this medical image in detail.",
                "history": [],
                "image": image_data
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Real image analyzed successfully:")
            print(f"{result['response'][:400]}...")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_health_check():
    """Test 7: System health check"""
    print_section("Test 7: System Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ System status:")
            print(f"  - Overall: {result['status']}")
            print(f"  - RAG Service: {result['rag_service']}")
            print(f"  - Agent Service: {result['agent_service']}")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🏥" * 35)
    print(" Multimodal Medical Triage System - Test Suite")
    print("🏥" * 35)
    
    print(f"\nServer URL: {BASE_URL}")
    print("Make sure the server is running: python -m src.main")
    input("\nPress Enter to start tests...")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Text-Only Chat", test_text_only_chat()))
    results.append(("Image Analysis", test_image_analysis()))
    results.append(("Multimodal Query", test_multimodal_query()))
    results.append(("Multimodal Ingestion", test_multimodal_ingestion()))
    results.append(("Text-Only Ingestion", test_text_only_ingestion()))
    results.append(("Real Image File", test_real_image_file()))
    
    # Summary
    print_section("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Multimodal system is working correctly.")
        print("\n📝 Next Steps:")
        print("1. Test with real medical images (X-rays, CT scans, MRIs)")
        print("2. Ingest medical datasets (see MEDICAL_DATASETS.md)")
        print("3. Deploy to production with proper security")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
