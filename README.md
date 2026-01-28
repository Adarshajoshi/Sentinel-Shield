🛡️ Sentinel-Shield: Enterprise AI Privacy Guardrail

The Problem
Enterprises are blocking GenAI tools (ChatGPT, Claude) because of Data Leakage. Employees accidentally share PII (Names, SSNs, API Keys), risking GDPR violations and security breaches.

The Solution
Sentinel-Shield is a high-performance AI Proxy. It intercepts user prompts, anonymizes sensitive data in real-time, and rehydrates the LLM's response so the user gets a personalized answer without the LLM ever seeing the private data.

🚀 Key Features
Multimodal PII Detection: Uses SpaCy (NLP) + Microsoft Presidio for 99% accuracy in entity recognition.

Contextual Rehydration: A secure, local vault maps placeholders (e.g., [PERSON_1]) back to original values post-inference.

Zero-Shot Custom Recognizers: Quickly add new protection rules for custom ID formats using Regex + Logic.

Performance First: Optimized middleware with sub-200ms overhead.

🏗️ System Architecture
User Input ──▶ [ Sentinel Proxy ] ──▶ [ LLM (Safe) ]
                    │      ▲               │
             (1) Mask PII  └─ (2) Unmask ──┘
                    │              │
              [ Secure Vault ] ◀───┘


🛠️ Tech Stack
Core: Python, Microsoft Presidio, SpaCy (en_core_web_lg)

API: FastAPI, Uvicorn

Environment: Docker

Monitoring: Arize Phoenix (LLM Observability)

🚦 Getting Started
1. Prerequisites
Python 3.10+

OpenAI API Key (or local LLM via Ollama)

2. Installation
# Clone the repo
git clone https://github.com/Adarshajoshi/sentinel-shield.git
cd sentinel-shield

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_lg

3. Run the Proxy
uvicorn main:app --reload

👨‍💻 Author
Adarsha Joshi AI/ML Student & Future AI Engineer 