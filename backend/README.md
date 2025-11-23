# Medical Triage System - Backend

A sophisticated AI-powered medical triage system built with LangChain, LangGraph, and OpenAI, featuring **multimodal** support (text + medical images), multi-agent workflows, RAG (Retrieval-Augmented Generation), and medical knowledge graphs.

## ✨ Key Features

- 🖼️ **Multimodal Support**: Analyze text + medical images (X-rays, CT scans, MRIs)
- 🤖 **Multi-Agent System**: 6 specialized agents with conditional routing
- 🔍 **Hybrid RAG**: Vector search + knowledge graph
- 👁️ **Vision AI**: OpenAI GPT-4 Vision for medical image analysis
- 📊 **LangSmith Tracing**: Complete workflow monitoring
- 💾 **Image Storage**: Automatic saving and retrieval of medical images

## 🏗️ Architecture

The system implements a multi-agent architecture based on the medical triage workflow:

### Agents

1. **Router Agent** - Validates if queries are medical-related (text/image)
2. **RAG Agent** - Analyzes images + searches knowledge base
3. **Triage Agent** - Assigns risk scores based on symptoms + imaging findings
4. **Self-Care Agent** - Provides advice for low-risk conditions
5. **Doctor Referral Agent** - Handles medium/high-risk cases requiring professional care
6. **Clarification Agent** - Asks follow-up questions when needed

### Technologies

- **LangChain**: Framework for LLM applications
- **LangGraph**: State machine for multi-agent workflows
- **LangSmith**: Monitoring and tracing for LLM applications
- **OpenAI GPT-4o-mini**: Text generation + vision analysis
- **ChromaDB**: Vector database for semantic search
- **NetworkX**: Knowledge graph implementation
- **FastAPI**: High-performance API framework

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key
- LangSmith API key (optional, for tracing)

## 🚀 Installation

### 1. Clone the repository

```bash
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your API keys:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# LangSmith Configuration (optional but recommended)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=medical-triage-system

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=medical_knowledge

# Application Settings
MAX_TOKENS=1000
TEMPERATURE=0.7
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 5. Initialize knowledge base

Run the initialization script to populate the medical knowledge base:

```bash
python init_knowledge.py
```

This will:
- Create the medical knowledge graph
- Ingest sample medical content (common cold, flu, COVID-19, etc.)
- Set up the vector store

## 🏃 Running the Server

### Development mode (with auto-reload)

```bash
python -m src.main
```

or

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production mode

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### `POST /chat`
Main medical triage endpoint with multimodal support.

**Request (Text only):**
```json
{
  "message": "I have a persistent cough and mild fever for 3 days",
  "history": [],
  "image": null
}
```

**Request (Text + Image):**
```json
{
  "message": "What do you see in this chest X-ray?",
  "history": [],
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response:**
```json
{
  "response": "Based on your symptoms... [and the X-ray findings showing...]"
}
```

#### `POST /ingest`
Add multimodal medical content to the knowledge base.

**Request (Text only):**
```json
{
  "text": "Medical content to add...",
  "source": "medical_article"
}
```

**Request (Text + Image):**
```json
{
  "text": "Patient presents with pneumonia. Chest X-ray shows opacity.",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "source": "radiology_case",
  "save_image": true
}
```

**Response:**
```json
{
  "success": true,
  "text_chunks": 3,
  "image_id": "a1b2c3d4e5f6g7h8",
  "image_analysis": "The chest X-ray shows...",
  "message": "Successfully ingested content with 3 chunks"
}
```

#### `GET /knowledge-graph/query?query=fever`
Query the knowledge graph directly.

#### `GET /knowledge-graph/search?query=headache&k=4`
Perform hybrid search (vector + graph).

#### `GET /health`
Health check endpoint.

## 🔍 LangSmith Monitoring

If configured, all agent interactions are traced in LangSmith:

1. Visit https://smith.langchain.com
2. Select your project (configured in LANGCHAIN_PROJECT)
3. View detailed traces of:
   - Agent routing decisions
   - RAG searches
   - Risk assessments
   - Response generation

## 🧪 Testing the System

### Test with cURL

```bash
# Basic chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have a headache and feel tired",
    "history": [],
    "image": null
  }'

# Health check
curl http://localhost:8000/health

# Query knowledge graph
curl "http://localhost:8000/knowledge-graph/query?query=fever"
```

### Example Queries

**Low-risk (Self-care advice):**
```
"I have a mild headache. What should I do?"
"My throat feels a bit scratchy"
```

**Medium-risk (Doctor consultation):**
```
"I've had a persistent cough for 2 weeks with some chest discomfort"
"My fever has been above 101°F for 4 days"
```

**With Medical Images:**
```python
import requests
import base64

# Load X-ray image
with open("chest_xray.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Send to chat endpoint
response = requests.post("http://localhost:8000/chat", json={
    "message": "I have chest pain and difficulty breathing. Here's my X-ray.",
    "image": f"data:image/jpeg;base64,{image_data}",
    "history": []
})

print(response.json()["response"])
```

**High-risk (Immediate attention):**
```
"I'm having severe chest pain and difficulty breathing"
"I have a sudden severe headache and confusion"
```

**Out of scope (Rejected):**
```
"What's the weather like today?"
"Tell me a joke"
```

## 🏥 Medical Knowledge Graph

The system includes a pre-built knowledge graph with:

**Entities:**
- Symptoms: fever, cough, headache, fatigue, chest pain, etc.
- Conditions: flu, COVID-19, pneumonia, bronchitis, migraine, etc.
- Treatments: rest, hydration, antibiotics, pain relievers, etc.

**Relationships:**
- Symptom → Condition (may_indicate)
- Condition → Treatment (treated_with)

You can expand this by:
1. Adding entities to `MedicalKnowledgeGraph._initialize_medical_knowledge()`
2. Ingesting more medical content via `/ingest` endpoint

## 📁 Project Structure

```
backend/
├── src/
│   ├── api/
│   │   ├── routes.py          # FastAPI endpoints
│   │   └── schemas.py         # Pydantic models
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── base.py            # Base classes (if any)
│   ├── services/
│   │   ├── agents/
│   │   │   └── service.py     # Multi-agent LangGraph system
│   │   └── rag/
│   │       └── service.py     # RAG + Knowledge Graph
│   └── main.py                # FastAPI application
├── init_knowledge.py          # Knowledge base initialization
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # This file
```

## 🔧 Customization

### Adding New Medical Knowledge

```python
# Add content via API
import requests

response = requests.post("http://localhost:8000/ingest", json={
    "text": "Your medical content here...",
    "source": "custom_source"
})
```

### Modifying Agent Behavior

Edit `src/services/agents/service.py` to customize:
- Risk scoring logic in `triage_agent`
- Response templates in `self_care_agent` and `doctor_referral_agent`
- Routing logic in conditional edges

### Adjusting Models

In `.env`:
```env
MODEL_NAME=gpt-4o  # Use GPT-4 for better quality
EMBEDDING_MODEL=text-embedding-3-large  # Better embeddings
TEMPERATURE=0.5  # More deterministic responses
```

## 📊 Medical Datasets

To enhance the system with real medical data, see **[MEDICAL_DATASETS.md](./MEDICAL_DATASETS.md)** for:

- 🩻 **Imaging Datasets**: ChestX-ray14, CheXpert, MIMIC-CXR, RSNA Pneumonia, MURA
- 📚 **Text Datasets**: PubMed, MedDialog, MedQuAD, Clinical Notes
- 🔬 **Multimodal**: ROCO, VQA-RAD, Medical Image + Caption datasets
- 📥 **Scripts**: Batch ingestion examples for various datasets

### Quick Start with Datasets

```python
# See init_multimodal_knowledge.py for examples
python init_multimodal_knowledge.py

# Or use the batch ingestion scripts in MEDICAL_DATASETS.md
```

## ⚠️ Important Notes

### Medical Disclaimer

This system is for educational and demonstration purposes only. It:
- Is NOT a substitute for professional medical advice
- Should NOT be used for actual medical diagnosis or treatment
- Always recommends consulting healthcare professionals for serious concerns
- Medical images require interpretation by licensed radiologists

### Data Privacy

- Medical images are stored locally in `./medical_images/`
- Patient queries are sent to OpenAI (review their privacy policy)
- For production use, implement proper data encryption and compliance (HIPAA, GDPR, etc.)
- Consider using Azure OpenAI for enhanced privacy and compliance

## 🐛 Troubleshooting

### "Import langchain_openai could not be resolved"
```bash
pip install langchain-openai
```

### "ChromaDB initialization error"
Delete the `chroma_db` directory and run `init_knowledge.py` again.

### "OpenAI rate limit exceeded"
- Check your OpenAI account usage limits
- Add retry logic or use a different model tier

### "LangSmith not tracing"
- Verify LANGCHAIN_API_KEY is set correctly
- Check that LANGCHAIN_TRACING_V2=true

## 📈 Performance

- Average response time: 2-5 seconds
- Concurrent requests: Supports multiple simultaneous users
- Vector search: Sub-second retrieval for 1000+ documents
- Knowledge graph queries: Near-instant

## 🚀 Deployment

### Docker (Recommended)

```bash
docker build -t medical-triage-backend .
docker run -p 8000:8000 --env-file .env medical-triage-backend
```

### Cloud Platforms

- **AWS**: Deploy on ECS or Lambda
- **Google Cloud**: Deploy on Cloud Run
- **Azure**: Deploy on App Service
- **Railway/Render**: One-click deployment

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review LangChain/LangGraph docs

---

Built with ❤️ using LangChain, LangGraph, and OpenAI
