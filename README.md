# 🧠 Adaptive AI Organizational Assistant (Local RAG Pipeline)

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker) ![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black) ![Google Workspace](https://img.shields.io/badge/Google_Workspace-OAuth_2.0-4285F4?logo=google) ![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-green)

An enterprise-grade, privacy-first Retrieval-Augmented Generation (RAG) pipeline designed to seamlessly integrate with Google Workspace. This assistant securely fetches live organizational data (emails, notes) and processes it entirely on local hardware, ensuring absolute data privacy with zero external API calls for inference.

## 🚀 Key Features

* **Privacy-First Architecture:** 100% local LLM inference using Ollama. No proprietary organizational data is ever sent to third-party APIs like OpenAI or Anthropic.
* **Live Workspace Integration:** Uses Google Workspace OAuth 2.0 to securely ingest live email data, dropping the need for static, hardcoded datasets.
* **Edge-Optimized Inference:** Engineered to run on standard hardware by utilizing lightweight, hyper-optimized models (Llama 3.2 1B / Mistral) to prevent Out-Of-Memory (OOM) errors while maintaining high reasoning capabilities.
* **Instantaneous UX:** Implements real-time token streaming to deliver ChatGPT-like responsiveness, masking underlying compute latency.
* **Containerized Deployment:** Fully Dockerized for cross-platform reproducibility, utilizing volume mounts for secure credential management.

## 🏗️ System Architecture

1. **Ingestion Layer:** Connects to the Gmail API via secure OAuth 2.0 flow to extract raw text payloads from recent emails.
2. **Embedding & Storage:** Uses `sentence-transformers` to vectorize text, storing high-dimensional embeddings in **FAISS** for rapid similarity search, alongside SQLite for metadata.
3. **Retrieval (RAG):** When a user asks a question, the system queries FAISS to instantly retrieve the top relevant context windows.
4. **Generation:** Passes the isolated context to a locally hosted LLM via Ollama, streaming the synthesized response back to the user.

## 🛠️ Tech Stack

* **Language:** Python 3.10
* **Infrastructure:** Docker, WSL (Windows Subsystem for Linux)
* **AI/ML:** Ollama (Llama 3.2 1B), HuggingFace `sentence-transformers`
* **Databases:** FAISS (Vector DB), SQLite (Relational DB)
* **APIs & Auth:** Google Cloud Console, Gmail API, OAuth 2.0

## 🚦 Prerequisites

Before running this project, ensure you have the following installed:
1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with WSL2 enabled if on Windows)
2. [Ollama](https://ollama.com/) running locally
3. A Google Cloud Console project with the Gmail API enabled and an OAuth 2.0 Client ID (`credentials.json`) downloaded.

## 💻 Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR-USERNAME/Adaptive-Org-Assistant-RAG.git](https://github.com/YOUR-USERNAME/Adaptive-Org-Assistant-RAG.git)
cd Adaptive-Org-Assistant-RAG
