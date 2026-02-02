# 🛡️ Sentinel-Shield

### **Enterprise-Grade PII Anonymization & Data Rehydration Middleware**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ed.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Sentinel-Shield** is a high-performance security layer designed to prevent data leakage when using Generative AI. It intercepts user prompts, masks sensitive information (PII/PHI) using a secure local Vault, and "rehydrates" the AI's response—allowing for personalized AI interactions without sensitive data ever leaving your secure environment.

---

## 🚀 Key Features

* **Dual-Layer Detection:** Leverages **SpaCy (NLP)** and **Microsoft Presidio** for enterprise-grade entity recognition.
* **Custom Enterprise Recognizers:** Out-of-the-box protection for proprietary ID formats (e.g., `PROJ-XXXX`) via custom Regex logic.
* **Contextual Rehydration:** A secure, in-memory Vault system that maps placeholders (e.g., `[PERSON_1]`) back to original values post-inference.
* **Performance First:** Optimized for real-time applications with a measured latency overhead of **<150ms**.
* **Observability & Auditing:** Automated logging of all redaction events (PII-free) for compliance and security monitoring.
* **Fail-Closed Architecture:** Implements strict error handling; if the privacy engine fails, the request is blocked to ensure zero data leaks.

---

## 🛠️ Tech Stack

* **Core Engine:** Python 3.10, Microsoft Presidio, SpaCy (`en_core_web_lg`)
* **User Interface:** Streamlit (Real-time Dashboard)
* **Infrastructure:** Docker

---

## 🚦 Getting Started

### **Option 1: Run with Docker (Recommended)**
Perfect for ensuring environment consistency and cloud readiness.

```bash
# Build the image
docker build -t sentinel-shield .

Access the dashboard at: http://localhost:8501

Option 2: Local Development
# Clone the repository
git clone [https://github.com/Adarshajoshi/Sentinel-Shield.git](https://github.com/Adarshajoshi/Sentinel-Shield.git)
cd sentinel-shield

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_lg

# Set PYTHONPATH and run the UI
# Windows (PowerShell):
$env:PYTHONPATH = "."
python -m streamlit run app/ui.py

# Run the container
docker run -p 8501:8501 sentinel-shield
