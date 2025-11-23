# Medical Dataset Sources

This document lists publicly available medical datasets that can be used to train and enhance the Medical Triage System. These datasets include both medical images (X-rays, CT scans, MRI, etc.) and text-based medical knowledge.

## 🏥 Medical Imaging Datasets

### 1. **ChestX-ray14 (NIH)**
- **Type**: Chest X-rays
- **Size**: 112,120 frontal-view X-ray images from 30,805 unique patients
- **Labels**: 14 different thoracic diseases
- **URL**: https://nihcc.app.box.com/v/ChestXray-NIHCC
- **Paper**: https://arxiv.org/abs/1705.02315
- **Use Case**: Pneumonia, tuberculosis, lung disease detection

### 2. **CheXpert (Stanford)**
- **Type**: Chest X-rays
- **Size**: 224,316 chest radiographs of 65,240 patients
- **Labels**: 14 observations (enlarged heart, pleural effusion, etc.)
- **URL**: https://stanfordmlgroup.github.io/competitions/chexpert/
- **License**: Research use with registration
- **Use Case**: Multi-disease chest X-ray classification

### 3. **MIMIC-CXR**
- **Type**: Chest X-rays + Radiology Reports
- **Size**: 377,110 images + 227,835 reports
- **URL**: https://physionet.org/content/mimic-cxr/2.0.0/
- **Requirements**: CITI training certificate required
- **Use Case**: Multimodal learning (image + text reports)

### 4. **RSNA Pneumonia Detection Challenge**
- **Type**: Chest X-rays
- **Size**: ~30,000 images
- **Labels**: Pneumonia detection with bounding boxes
- **URL**: https://www.kaggle.com/c/rsna-pneumonia-detection-challenge
- **License**: Kaggle competition (free)
- **Use Case**: Pneumonia detection and localization

### 5. **COVID-19 Chest X-ray Dataset**
- **Type**: Chest X-rays
- **Size**: 21,165 images (COVID, Normal, Viral Pneumonia, Bacterial Pneumonia)
- **URL**: https://www.kaggle.com/datasets/prashant268/chest-xray-covid19-pneumonia
- **License**: Public
- **Use Case**: COVID-19 detection

### 6. **MURA (Musculoskeletal Radiographs)**
- **Type**: X-rays (bone, joint)
- **Size**: 40,561 images from 14,863 studies
- **Labels**: Abnormal vs. normal
- **URL**: https://stanfordmlgroup.github.io/competitions/mura/
- **Body Parts**: Finger, hand, wrist, elbow, forearm, humerus, shoulder
- **Use Case**: Fracture and abnormality detection

### 7. **BraTS (Brain Tumor Segmentation)**
- **Type**: MRI scans
- **Size**: ~600 cases per year
- **Labels**: Glioma segmentation masks
- **URL**: http://braintumorsegmentation.org/
- **Use Case**: Brain tumor detection and segmentation

### 8. **LIDC-IDRI (Lung Nodules)**
- **Type**: CT scans
- **Size**: 1,018 cases with lung nodule annotations
- **URL**: https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI
- **Use Case**: Lung cancer screening and nodule detection

### 9. **Retinal Fundus Images**
- **Type**: Retinal photographs
- **Datasets**:
  - **APTOS 2019**: Diabetic retinopathy (3,662 images) - https://www.kaggle.com/c/aptos2019-blindness-detection
  - **Messidor**: Diabetic retinopathy (1,200 images) - http://www.adcis.net/en/third-party/messidor/
  - **EyePACS**: 88,702 retinal images - https://www.kaggle.com/c/diabetic-retinopathy-detection
- **Use Case**: Diabetic retinopathy, glaucoma detection

### 10. **ISIC Archive (Skin Lesions)**
- **Type**: Dermoscopy images
- **Size**: 100,000+ images
- **Labels**: Melanoma, nevus, basal cell carcinoma, etc.
- **URL**: https://www.isic-archive.com/
- **Use Case**: Skin cancer detection

---

## 📚 Medical Text Datasets

### 1. **PubMed Central (PMC)**
- **Type**: Full-text medical articles
- **Size**: 7+ million full-text articles
- **URL**: https://www.ncbi.nlm.nih.gov/pmc/tools/ftp/
- **License**: Open Access subset available
- **Use Case**: Medical knowledge base, literature extraction

### 2. **MedDialog**
- **Type**: Doctor-patient conversations
- **Size**: 260,000+ conversations (English and Chinese)
- **URL**: https://github.com/UCSD-AI4H/Medical-Dialogue-System
- **Use Case**: Training conversational medical AI

### 3. **MedQuAD (Medical Question Answering)**
- **Type**: Question-answer pairs
- **Size**: 47,457 QA pairs
- **Sources**: NIH websites (MedlinePlus, CDC, etc.)
- **URL**: https://github.com/abachaa/MedQuAD
- **Use Case**: Medical Q&A systems

### 4. **HealthSearchQA**
- **Type**: Consumer health questions + web search results
- **Size**: 3,173 questions with relevance judgments
- **URL**: https://github.com/clulab/healthsearchqa
- **Use Case**: Health information retrieval

### 5. **i2b2 Clinical Notes**
- **Type**: De-identified clinical notes
- **Challenges**: Multiple challenges (2006-2014)
- **URL**: https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/
- **Requirements**: Data Use Agreement required
- **Use Case**: Clinical NLP, entity extraction

### 6. **MIMIC-III Clinical Notes**
- **Type**: ICU patient records with clinical notes
- **Size**: 2 million+ notes from 46,000+ patients
- **URL**: https://physionet.org/content/mimiciii/1.4/
- **Requirements**: CITI training certificate
- **Use Case**: Clinical prediction, NLP

### 7. **UMLS (Unified Medical Language System)**
- **Type**: Medical terminology, ontologies
- **Size**: 4+ million concepts from 200+ sources
- **URL**: https://www.nlm.nih.gov/research/umls/
- **License**: Free with license agreement
- **Use Case**: Medical entity linking, knowledge graphs

### 8. **Medical Transcriptions**
- **Type**: Clinical transcriptions across specialties
- **Size**: 5,000+ transcriptions
- **URL**: https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions
- **Specialties**: 40+ medical specialties
- **Use Case**: Clinical NLP, specialty classification

### 9. **PMC-Patients**
- **Type**: Patient case reports
- **Size**: 167,000+ patient-article pairs
- **URL**: https://github.com/zhao-zy15/PMC-Patients
- **Use Case**: Clinical case retrieval, diagnosis support

### 10. **DDXPlus**
- **Type**: Differential diagnosis dataset
- **Size**: 1.3 million synthetic patient cases
- **URL**: https://figshare.com/articles/dataset/DDXPlus_Dataset/20043374
- **Use Case**: Symptom-based diagnosis prediction

---

## 🔬 Multimodal Medical Datasets

### 1. **ROCO (Radiology Objects in COntext)**
- **Type**: Medical images + captions
- **Size**: 81,825 images with captions
- **URL**: https://github.com/razorx89/roco-dataset
- **Use Case**: Image captioning, visual question answering

### 2. **VQA-RAD**
- **Type**: Radiology images + questions + answers
- **Size**: 3,515 QA pairs on 315 images
- **URL**: https://osf.io/89kps/
- **Use Case**: Visual question answering in radiology

### 3. **Med-VQA**
- **Type**: Medical images + questions
- **Size**: Multiple datasets (VQA-Med, PathVQA, etc.)
- **URL**: https://www.imageclef.org/2021/medical/vqa
- **Use Case**: Multimodal medical QA

### 4. **OpenPath**
- **Type**: Pathology images + text descriptions
- **Size**: 208,000+ images
- **URL**: https://laion.ai/blog/open-path/
- **Use Case**: Pathology image understanding

---

## 📥 How to Use These Datasets

### Step 1: Download and Prepare Data

```python
# Example: Ingesting chest X-ray with radiology report

import base64
from pathlib import Path

# Load X-ray image
image_path = "path/to/chest_xray.jpg"
with open(image_path, "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Load corresponding report
report = """
FINDINGS: Chest X-ray shows opacity in the right lower lobe consistent with pneumonia.
Heart size is normal. No pleural effusion or pneumothorax.

IMPRESSION: Right lower lobe pneumonia.
"""

# Send to ingestion endpoint
import requests

response = requests.post("http://localhost:8000/ingest", json={
    "text": report,
    "image": f"data:image/jpeg;base64,{image_data}",
    "source": "chest_xray_dataset",
    "save_image": True
})

print(response.json())
```

### Step 2: Batch Ingestion Script

```python
# batch_ingest.py

import os
import base64
import requests
from pathlib import Path
import pandas as pd
from tqdm import tqdm

def ingest_dataset(image_dir, metadata_csv, base_url="http://localhost:8000"):
    """
    Batch ingest medical images with metadata
    
    Args:
        image_dir: Directory containing images
        metadata_csv: CSV with columns: filename, report, diagnosis
    """
    df = pd.read_csv(metadata_csv)
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        image_path = Path(image_dir) / row['filename']
        
        if not image_path.exists():
            continue
        
        # Load image
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
        
        # Prepare text
        text = f"""
        Diagnosis: {row['diagnosis']}
        
        Report: {row['report']}
        """
        
        # Ingest
        try:
            response = requests.post(f"{base_url}/ingest", json={
                "text": text,
                "image": f"data:image/jpeg;base64,{image_data}",
                "source": f"dataset_{row['filename']}",
                "save_image": True
            })
            
            if response.status_code != 200:
                print(f"Error ingesting {row['filename']}: {response.text}")
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    ingest_dataset(
        image_dir="./data/chest_xrays",
        metadata_csv="./data/metadata.csv"
    )
```

### Step 3: Create Medical Knowledge Base from PubMed

```python
# pubmed_ingestion.py

from Bio import Entrez
import requests

Entrez.email = "your.email@example.com"

def fetch_pubmed_articles(query, max_results=100):
    """Fetch articles from PubMed"""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

def get_article_text(pmid):
    """Get article abstract"""
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
    return handle.read()

def ingest_pubmed_knowledge(topics, base_url="http://localhost:8000"):
    """Ingest PubMed articles for medical topics"""
    
    for topic in topics:
        print(f"Fetching articles for: {topic}")
        
        pmids = fetch_pubmed_articles(topic, max_results=50)
        
        for pmid in pmids:
            try:
                article = get_article_text(pmid)
                
                response = requests.post(f"{base_url}/ingest", json={
                    "text": article,
                    "source": f"pubmed_{topic}_{pmid}"
                })
                
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    medical_topics = [
        "pneumonia treatment",
        "diabetes management",
        "hypertension guidelines",
        "COVID-19 symptoms",
        "migraine treatment"
    ]
    
    ingest_pubmed_knowledge(medical_topics)
```

---

## ⚖️ Legal and Ethical Considerations

1. **Data Use Agreements**: Many datasets require signing agreements
2. **HIPAA Compliance**: Ensure patient data is de-identified
3. **Licensing**: Check licenses before commercial use
4. **Citations**: Cite datasets in publications
5. **Bias**: Be aware of demographic biases in medical datasets
6. **Validation**: Always validate AI outputs with medical professionals

---

## 🚀 Recommended Starting Point

For this project, we recommend starting with:

1. **ChestX-ray14** or **CheXpert** for X-ray images
2. **MedQuAD** for medical Q&A pairs
3. **Medical Transcriptions** for clinical text
4. **COVID-19 datasets** for recent, relevant data

These are publicly available and don't require extensive approval processes.

---

## 📧 Contact Information

For dataset access issues or questions:
- NIH datasets: https://www.nih.gov/
- Stanford ML Group: https://stanfordmlgroup.github.io/
- PhysioNet: https://physionet.org/about/contact/

---

## 🔗 Additional Resources

- **Medical Imaging Repository**: https://www.cancerimagingarchive.net/
- **Kaggle Medical Datasets**: https://www.kaggle.com/datasets?tags=13302-Healthcare
- **HuggingFace Medical**: https://huggingface.co/datasets?task_categories=task_categories:medical
- **Papers with Code Medical**: https://paperswithcode.com/area/medical
