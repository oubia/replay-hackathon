#!/usr/bin/env python3
"""
Test script for the Medical Triage System

Run this after starting the server to verify all components work correctly.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def test_health_check():
    """Test the health check endpoint"""
    print_section("Testing Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat(message, description):
    """Test the chat endpoint"""
    print_section(f"Testing Chat: {description}")
    print(f"Query: {message}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": message,
                "history": [],
                "image": None
            }
        )
        
        print(f"\nStatus: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"\nResponse:\n{result['response']}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_knowledge_graph_query():
    """Test the knowledge graph query endpoint"""
    print_section("Testing Knowledge Graph Query")
    
    query = "fever"
    print(f"Query: {query}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/knowledge-graph/query",
            params={"query": query}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_hybrid_search():
    """Test the hybrid search endpoint"""
    print_section("Testing Hybrid Search")
    
    query = "cough and fever"
    print(f"Query: {query}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/knowledge-graph/search",
            params={"query": query, "k": 3}
        )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        
        # Print vector results
        print(f"\nVector Results ({len(result['results']['vector_results'])} found):")
        for i, vr in enumerate(result['results']['vector_results'][:2], 1):
            print(f"\n{i}. Score: {vr['score']:.4f}")
            print(f"   Content: {vr['content'][:150]}...")
        
        # Print graph results
        print(f"\nGraph Results:")
        print(result['results']['graph_results'])
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ingest():
    """Test the ingest endpoint"""
    print_section("Testing Content Ingestion")
    
    medical_content = """
    Strep Throat is a bacterial infection that causes inflammation and pain in the throat.
    
    Symptoms include:
    - Severe sore throat
    - Painful swallowing
    - Fever
    - Red and swollen tonsils
    - Swollen lymph nodes in neck
    
    Treatment requires antibiotics prescribed by a doctor.
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/ingest",
            json={
                "text": medical_content,
                "source": "test_ingestion"
            }
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🏥" * 30)
    print("Medical Triage System - Test Suite")
    print("🏥" * 30)
    
    print(f"\nServer URL: {BASE_URL}")
    print("Make sure the server is running before proceeding.")
    input("\nPress Enter to start tests...")
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Out of scope query (should be rejected)
    results.append((
        "Out of Scope Query",
        test_chat(
            "What's the weather today?",
            "Out of scope (should reject)"
        )
    ))
    
    # Test 3: Low-risk query (self-care)
    results.append((
        "Low-Risk Query",
        test_chat(
            "I have a mild headache. What can I do?",
            "Low-risk symptoms (self-care advice)"
        )
    ))
    
    # Test 4: Medium-risk query (doctor consultation)
    results.append((
        "Medium-Risk Query",
        test_chat(
            "I've had a persistent cough for 2 weeks with some chest discomfort",
            "Medium-risk symptoms (doctor referral)"
        )
    ))
    
    # Test 5: High-risk query (immediate attention)
    results.append((
        "High-Risk Query",
        test_chat(
            "I'm experiencing severe chest pain and difficulty breathing",
            "High-risk symptoms (emergency)"
        )
    ))
    
    # Test 6: Knowledge graph query
    results.append(("Knowledge Graph Query", test_knowledge_graph_query()))
    
    # Test 7: Hybrid search
    results.append(("Hybrid Search", test_hybrid_search()))
    
    # Test 8: Content ingestion
    results.append(("Content Ingestion", test_ingest()))
    
    # Summary
    print_section("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")
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
