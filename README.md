# 🤖 Adaptive AI-Based Organizational Assistant

A privacy-first, fully local Retrieval-Augmented Generation (RAG) assistant designed to consolidate organizational data (emails, calendars, team updates) and provide context-aware insights through an interactive Executive Dashboard.

This project was specifically optimized to run complex LLMs locally on consumer-grade hardware (RTX 3050 6GB VRAM) using 4-bit quantization and efficient vector similarity search.

## ✨ Key Features
* **100% Local Inference:** Zero cloud API dependencies. All data processing and LLM reasoning occur on-device for maximum privacy.
* **Entity Resolution Logic:** Custom constraint-based prompt engineering solves the "Shared Identity" problem (hallucinations caused by shared organizational mailboxes).
* **Asynchronous Executive Dashboard:** Parallel data fetching populates Sprint Progress, Team PTO, and Project Blockers simultaneously without freezing the chat UI.
* **Hardware Telemetry:** Real-time UI sidebar tracking GPU VRAM usage and RAG parameters (Top-K, Chunk Size).
* **Glassmorphism UI:** A premium, dark-mode interface with dynamic markdown rendering (`marked.js`) and a Source Transparency module to verify retrieved context.

## 🛠️ Tech Stack
* **Frontend:** HTML5, CSS3 (Glassmorphism), Vanilla JavaScript, `marked.js`
* **Backend API:** Python, Flask, Flask-CORS
* **Embedding Model:** `SentenceTransformers` (`all-MiniLM-L6-v2`)
* **Vector Database:** `FAISS` (IndexFlatL2)
* **Local LLM Engine:** `Ollama` (Running `llama3.2:3b` / `llama3.1:8b` in INT4)

---

## 🚀 Getting Started

### 1. Prerequisites
* **Python 3.8+** installed
* **Ollama** installed (Download from [ollama.com](https://ollama.com/))
* A system with at least 8GB RAM (A dedicated GPU with 6GB+ VRAM like an RTX 3050 is highly recommended for optimal speed).

### 2. Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/231b118/Adaptive-Org-Assistant-RAG.git](https://github.com/231b118/Adaptive-Org-Assistant-RAG.git)
   cd Adaptive-Org-Assistant-RAG
