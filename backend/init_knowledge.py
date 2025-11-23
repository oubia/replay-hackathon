#!/usr/bin/env python3
"""
Medical Knowledge Initializer

This script initializes the medical knowledge base with sample medical information.
Run this once after setting up the environment to populate the vector store.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from src.services.rag.service import ChromaRAGService
from src.core.config import settings

# Sample medical knowledge
MEDICAL_KNOWLEDGE = [
    {
        "title": "Common Cold",
        "content": """
        The common cold is a viral infection of the upper respiratory tract. 
        
        Symptoms:
        - Runny or stuffy nose
        - Sore throat
        - Cough
        - Mild headache
        - Sneezing
        - Low-grade fever (occasional)
        
        Treatment:
        - Rest and stay hydrated
        - Over-the-counter pain relievers for aches
        - Throat lozenges for sore throat
        - Usually resolves in 7-10 days
        
        When to see a doctor:
        - Symptoms lasting more than 10 days
        - High fever above 101.3°F (38.5°C)
        - Difficulty breathing
        - Severe throat pain
        """
    },
    {
        "title": "Influenza (Flu)",
        "content": """
        Influenza is a viral infection that attacks the respiratory system.
        
        Symptoms:
        - Sudden onset of fever (usually high)
        - Chills and sweats
        - Muscle aches
        - Headache
        - Dry, persistent cough
        - Fatigue and weakness
        - Nasal congestion
        
        Treatment:
        - Antiviral medications (if started within 48 hours)
        - Rest and plenty of fluids
        - Fever reducers and pain relievers
        - Usually improves in 1-2 weeks
        
        Complications:
        - Pneumonia
        - Bronchitis
        - Ear infections
        - Severe cases require immediate medical attention
        """
    },
    {
        "title": "COVID-19",
        "content": """
        COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus.
        
        Common Symptoms:
        - Fever or chills
        - Cough
        - Shortness of breath
        - Fatigue
        - Muscle or body aches
        - Loss of taste or smell
        - Sore throat
        - Congestion or runny nose
        
        Severe Symptoms (Seek Emergency Care):
        - Difficulty breathing
        - Persistent chest pain or pressure
        - Confusion
        - Inability to wake or stay awake
        - Bluish lips or face
        
        Treatment:
        - Most cases: rest, fluids, over-the-counter medications
        - Severe cases: hospitalization may be required
        - Antiviral treatments available for high-risk patients
        - Get tested if you have symptoms or were exposed
        """
    },
    {
        "title": "Pneumonia",
        "content": """
        Pneumonia is an infection that inflames air sacs in one or both lungs.
        
        Symptoms:
        - Chest pain when breathing or coughing
        - Cough with phlegm or pus
        - Fever, sweating, and chills
        - Shortness of breath
        - Fatigue
        - Nausea, vomiting, or diarrhea
        
        Risk Factors:
        - Age (very young or over 65)
        - Chronic diseases
        - Weakened immune system
        - Smoking
        
        Treatment:
        - Antibiotics for bacterial pneumonia
        - Rest and fluids
        - Fever reducers
        - Hospitalization for severe cases
        - Oxygen therapy if needed
        
        This condition requires medical evaluation and treatment.
        """
    },
    {
        "title": "Migraine",
        "content": """
        Migraine is a neurological condition causing intense, debilitating headaches.
        
        Symptoms:
        - Intense throbbing pain, usually on one side
        - Nausea and vomiting
        - Sensitivity to light and sound
        - Visual disturbances (aura)
        - Dizziness
        - Duration: 4-72 hours
        
        Triggers:
        - Stress
        - Certain foods
        - Hormonal changes
        - Sleep changes
        - Weather changes
        
        Treatment:
        - Pain relievers (taken early)
        - Triptans (prescription)
        - Anti-nausea medications
        - Rest in quiet, dark room
        - Preventive medications for frequent migraines
        
        Consult a doctor if:
        - Headaches interfere with daily life
        - Sudden, severe headache
        - Headache with fever, stiff neck, confusion
        """
    },
    {
        "title": "Hypertension (High Blood Pressure)",
        "content": """
        Hypertension is persistently elevated blood pressure in the arteries.
        
        Normal Blood Pressure: Less than 120/80 mm Hg
        Elevated: 120-129 systolic and less than 80 diastolic
        Hypertension Stage 1: 130-139 systolic or 80-89 diastolic
        Hypertension Stage 2: 140/90 mm Hg or higher
        
        Often No Symptoms:
        - Called the "silent killer"
        - May cause headaches in severe cases
        - Can lead to heart disease, stroke, kidney problems
        
        Management:
        - Healthy diet (less sodium)
        - Regular exercise
        - Weight management
        - Stress reduction
        - Limit alcohol
        - Quit smoking
        - Medications if lifestyle changes aren't enough
        
        Regular monitoring is essential.
        """
    },
    {
        "title": "Type 2 Diabetes",
        "content": """
        Type 2 diabetes is a chronic condition affecting how the body processes blood sugar.
        
        Symptoms:
        - Increased thirst
        - Frequent urination
        - Increased hunger
        - Unintended weight loss
        - Fatigue
        - Blurred vision
        - Slow-healing sores
        - Frequent infections
        
        Risk Factors:
        - Overweight or obesity
        - Sedentary lifestyle
        - Family history
        - Age over 45
        - Prediabetes
        
        Management:
        - Healthy eating
        - Regular exercise
        - Weight loss
        - Blood sugar monitoring
        - Medications or insulin
        - Regular medical checkups
        
        Complications if uncontrolled:
        - Heart disease
        - Kidney disease
        - Eye problems
        - Nerve damage
        """
    },
    {
        "title": "Anxiety Disorders",
        "content": """
        Anxiety disorders involve excessive fear or worry that interferes with daily activities.
        
        Physical Symptoms:
        - Rapid heartbeat
        - Sweating
        - Trembling
        - Shortness of breath
        - Chest pain
        - Dizziness
        - Fatigue
        
        Mental Symptoms:
        - Excessive worry
        - Restlessness
        - Difficulty concentrating
        - Irritability
        - Sleep problems
        
        Treatment:
        - Psychotherapy (cognitive behavioral therapy)
        - Medications (anti-anxiety, antidepressants)
        - Lifestyle changes:
          * Regular exercise
          * Adequate sleep
          * Stress management
          * Avoiding alcohol and caffeine
        - Relaxation techniques
        - Support groups
        
        Seek help if anxiety interferes with your life.
        """
    },
    {
        "title": "Bronchitis",
        "content": """
        Bronchitis is inflammation of the bronchial tubes carrying air to the lungs.
        
        Acute Bronchitis Symptoms:
        - Cough (may produce mucus)
        - Fatigue
        - Shortness of breath
        - Slight fever and chills
        - Chest discomfort
        - Usually lasts 3-10 days
        
        Chronic Bronchitis:
        - Cough lasting 3+ months
        - Recurring over 2+ years
        - Often related to smoking
        
        Treatment:
        - Rest and fluids
        - Humidifier use
        - Cough medicine (if recommended)
        - Avoid lung irritants
        - Bronchodilators if wheezing
        - Antibiotics only if bacterial infection
        
        See a doctor if:
        - Cough lasts more than 3 weeks
        - High fever
        - Bloody mucus
        - Difficulty breathing
        """
    },
    {
        "title": "Dehydration",
        "content": """
        Dehydration occurs when you lose more fluid than you take in.
        
        Mild to Moderate Symptoms:
        - Increased thirst
        - Dry mouth
        - Tired or sleepy
        - Decreased urine output
        - Dark colored urine
        - Headache
        - Dry skin
        
        Severe Symptoms (Seek Emergency Care):
        - Extreme thirst
        - Very dry mouth, skin, and mucous membranes
        - Little or no urination
        - Sunken eyes
        - Low blood pressure
        - Rapid heartbeat
        - Rapid breathing
        - Fever
        - Confusion or irritability
        
        Treatment:
        - Drink water or oral rehydration solutions
        - Avoid caffeinated and alcoholic beverages
        - Rest in a cool place
        - Severe cases: IV fluids in medical setting
        
        Prevention:
        - Drink plenty of water daily
        - Increase fluids during hot weather or exercise
        - Monitor urine color (should be pale yellow)
        """
    }
]

def initialize_knowledge_base():
    """Initialize the medical knowledge base"""
    print("Initializing Medical Knowledge Base...")
    print(f"Using model: {settings.model_name}")
    print(f"Using embeddings: {settings.embedding_model}")
    print(f"Persist directory: {settings.chroma_persist_directory}")
    print()
    
    # Initialize RAG service
    print("Creating RAG service...")
    rag_service = ChromaRAGService()
    print("✓ RAG service created")
    print(f"✓ Knowledge graph initialized with medical entities")
    print()
    
    # Ingest medical knowledge
    print("Ingesting medical knowledge...")
    total_chunks = 0
    
    for i, knowledge in enumerate(MEDICAL_KNOWLEDGE, 1):
        title = knowledge["title"]
        content = f"# {title}\n\n{knowledge['content']}"
        
        print(f"  [{i}/{len(MEDICAL_KNOWLEDGE)}] Ingesting: {title}...")
        chunks = rag_service.ingest_text(content, source=f"medical_kb_{title.lower().replace(' ', '_')}")
        total_chunks += chunks
        print(f"     ✓ Added {chunks} chunks")
    
    print()
    print(f"✓ Successfully ingested {len(MEDICAL_KNOWLEDGE)} medical topics")
    print(f"✓ Total chunks created: {total_chunks}")
    print()
    print("Knowledge base initialization complete!")
    print()
    print("You can now start the backend server:")
    print("  python -m src.main")

if __name__ == "__main__":
    try:
        initialize_knowledge_base()
    except Exception as e:
        print(f"✗ Error initializing knowledge base: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
