# Quick Reference: Multimodal Medical Triage System

## 🚀 Quick Start

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Configure API keys in .env
OPENAI_API_KEY=sk-...
LANGCHAIN_API_KEY=lsv2_pt_...

# 3. Initialize knowledge base
python init_knowledge.py

# 4. Start server
python -m src.main

# 5. Test multimodal features
python test_multimodal.py
```

## 💬 API Usage Examples

### Text-Only Query
```python
import requests

response = requests.post("http://localhost:8000/chat", json={
    "message": "I have a headache and fever",
    "history": [],
    "image": None
})
```

### Image-Only Query
```python
import base64

with open("xray.jpg", "rb") as f:
    img = base64.b64encode(f.read()).decode()

response = requests.post("http://localhost:8000/chat", json={
    "message": "What do you see in this image?",
    "image": f"data:image/jpeg;base64,{img}"
})
```

### Multimodal Query (Text + Image)
```python
response = requests.post("http://localhost:8000/chat", json={
    "message": "I have chest pain. Here's my X-ray.",
    "image": f"data:image/jpeg;base64,{img}"
})
```

### Ingest Medical Content
```python
# Text only
response = requests.post("http://localhost:8000/ingest", json={
    "text": "Medical knowledge text...",
    "source": "article_001"
})

# Text + Image
response = requests.post("http://localhost:8000/ingest", json={
    "text": "Radiology report...",
    "image": f"data:image/jpeg;base64,{img}",
    "source": "radiology_001",
    "save_image": True
})
```

## 📂 File Structure

```
backend/
├── .env                          # API keys and config
├── requirements.txt              # Python dependencies
├── README.md                     # Full documentation
├── MEDICAL_DATASETS.md          # Dataset sources (30+)
├── MULTIMODAL_IMPLEMENTATION.md # Implementation details
├── init_knowledge.py            # Text-only initialization
├── init_multimodal_knowledge.py # Multimodal initialization
├── test_system.py               # Original test suite
├── test_multimodal.py          # Multimodal test suite
└── src/
    ├── main.py                  # FastAPI app
    ├── core/
    │   └── config.py           # Settings (vision model, image storage)
    ├── api/
    │   ├── routes.py           # Endpoints (chat, ingest)
    │   └── schemas.py          # Request/response models
    └── services/
        ├── rag/
        │   └── service.py      # RAG + multimodal ingestion
        ├── agents/
        │   └── service.py      # Multi-agent system
        └── vision/
            └── image_processor.py  # Image analysis & storage
```

## 🔑 Key Configuration (.env)

```env
# OpenAI
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o-mini
VISION_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# LangSmith (optional)
LANGCHAIN_API_KEY=lsv2_pt_...
LANGCHAIN_TRACING_V2=true

# Storage
CHROMA_PERSIST_DIRECTORY=./chroma_db
IMAGE_STORAGE_DIR=./medical_images
MAX_IMAGE_SIZE_MB=10
```

## 📊 Medical Datasets (Top Picks)

| Dataset | Type | Size | Link |
|---------|------|------|------|
| **ChestX-ray14** | X-rays | 112K images | NIH |
| **CheXpert** | X-rays | 224K images | Stanford |
| **MIMIC-CXR** | X-rays + Reports | 377K + 227K | PhysioNet |
| **MedQuAD** | Q&A | 47K pairs | GitHub |
| **ROCO** | Image + Caption | 81K | GitHub |

Full list: See [MEDICAL_DATASETS.md](./MEDICAL_DATASETS.md)

## 🧪 Testing

```bash
# Test complete system (7 tests)
python test_multimodal.py

# Test with real image
# 1. Save image as test_xray.jpg
# 2. Run test_multimodal.py
```

## 🔍 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Status + agent list |
| `/health` | GET | Health check |
| `/chat` | POST | Multimodal medical query |
| `/ingest` | POST | Add content + images |
| `/knowledge-graph/query` | GET | Query graph |
| `/knowledge-graph/search` | GET | Hybrid search |
| `/docs` | GET | Swagger UI |

## 🎯 Agent Workflow

```
User Query (text + image)
    ↓
Router Agent: Medical relevance? ✓
    ↓
RAG Agent: Analyze image + search knowledge
    ↓
Triage Agent: Risk assessment (0-10)
    ↓
    ├─→ Low (0-3): Self-Care Agent
    ├─→ Medium (4-6): Doctor Referral Agent
    └─→ High (7-10): Emergency Referral Agent
```

## 💡 Quick Tips

**Image Preparation:**
```python
# Load and encode image
import base64
with open("image.jpg", "rb") as f:
    img = base64.b64encode(f.read()).decode()
    img_data = f"data:image/jpeg;base64,{img}"
```

**Batch Ingestion:**
```python
from pathlib import Path

for img_path in Path("dataset").glob("*.jpg"):
    with open(img_path, "rb") as f:
        img = base64.b64encode(f.read()).decode()
    
    response = requests.post("http://localhost:8000/ingest", json={
        "image": f"data:image/jpeg;base64,{img}",
        "source": img_path.stem
    })
```

**Check Image Storage:**
```bash
ls -lh medical_images/          # View stored images
cat medical_images/metadata/*.json  # View metadata
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Import errors | `pip install -r requirements.txt` |
| Vision API error | Check OPENAI_API_KEY and VISION_MODEL |
| Image too large | Resize or adjust MAX_IMAGE_SIZE_MB |
| ChromaDB error | Delete `chroma_db/` and re-run `init_knowledge.py` |
| No image analysis | Verify base64 encoding and image format |

## 📖 Documentation Links

- **Full Setup**: [README.md](./README.md)
- **Medical Datasets**: [MEDICAL_DATASETS.md](./MEDICAL_DATASETS.md)
- **Implementation Details**: [MULTIMODAL_IMPLEMENTATION.md](./MULTIMODAL_IMPLEMENTATION.md)
- **API Docs**: http://localhost:8000/docs (when running)
- **LangSmith**: https://smith.langchain.com

## ⚠️ Important Notes

- **Educational Use Only**: Not for actual medical diagnosis
- **Privacy**: De-identify images before upload
- **Compliance**: HIPAA/GDPR required for production
- **Validation**: Always verify AI outputs with medical professionals
- **Image Quality**: Use high-resolution medical images

## 🎓 Learning Resources

1. **LangChain Docs**: https://python.langchain.com/
2. **LangGraph Tutorial**: https://langchain-ai.github.io/langgraph/
3. **OpenAI Vision API**: https://platform.openai.com/docs/guides/vision
4. **Medical AI Papers**: https://paperswithcode.com/area/medical

---

**Need Help?** Check the full documentation or run `python test_multimodal.py` to verify your setup.
