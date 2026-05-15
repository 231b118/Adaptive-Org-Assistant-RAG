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

**i. Clone the repository:**
 ```bash
   git clone https://github.com/231b118/Adaptive-Org-Assistant-RAG.git
   cd Adaptive-Org-Assistant-RAG
   ```
   Set up a Python Virtual Environment :
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
**ii. Install Required Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Otherwise, install the packages manually:
   ```bash
   pip install flask flask-cors sentence-transformers faiss-cpu numpy requests
   ```
   (Note: If you have an NVIDIA GPU and CUDA installed, you can install faiss-gpu instead of faiss-cpu for significantly       faster vector searches).

**iii. Download the Local LLM:**
* Make sure the Ollama application is running on your machine, then open a terminal and pull the 3B model:

   ```bash
   ollama pull llama3.2
   ```

**iv. Running the Application:**
*  Step 1: Start the Backend Server
   Keep Ollama running in the background. Open a terminal in your project folder and start the Flask API:

   ```bash
   python server.py
   ```
   (The server should now be listening on http://localhost:5000)

*  Step 2: Launch the Interface
   Simply open the index.html file in your preferred web browser.
   (For the best experience, use a local development server like the "Live Server" extension in VS Code).
