# 🧠 Adaptive AI Organizational Assistant (Local RAG Pipeline)

> An enterprise-grade, privacy-first Retrieval-Augmented Generation (RAG) system. This intelligent assistant ingests unstructured corporate data, processes it via semantic search, and provides hallucination-free insights using a locally hosted Large Language Model.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Ollama](https://img.shields.io/badge/AI_Engine-Ollama_|_Mistral_7B-white.svg)
![FAISS](https://img.shields.io/badge/Vector_DB-FAISS-green.svg)
![SQLite](https://img.shields.io/badge/Relational_DB-SQLite-lightgrey.svg)

## ✨ Key Features

* 🔒 **100% Local & Private:** Inference is handled locally via Ollama. Sensitive organizational data (emails, meetings, internal blockers) never leaves your machine.
* 🗄️ **Decoupled Dual-Database Architecture:** Pairs **FAISS** for sub-millisecond high-dimensional vector similarity search with **SQLite** for persistent, relational payload retrieval.
* 🔄 **Data Normalization Layer:** Intelligently unifies disparate data schemas (RFC-822 Emails, nested JSON Calendar Events, Jira Tasks) into a standardized semantic vector space.
* 🛡️ **Production-Ready Security:** Implements `.env` configurations to ensure secure, credential-free code commits.

## 🏗️ System Architecture

1. **Ingestion & Normalization:** Extracts live data from external APIs/IMAP, cleans it using Regex, and tags it with contextual metadata.
2. **Semantic Translation:** Passes cleaned text through `all-MiniLM-L6-v2` (`sentence-transformers`) to generate 384-dimensional vector embeddings.
3. **Index & Store:** Maps the exact mathematical vectors in FAISS to the English text payloads stored securely in SQLite via shared Primary Keys.
4. **Retrieval-Augmented Generation:** * Embeds user queries.
   * Performs an L2-distance search in FAISS to find the top-K relevant documents.
   * Injects the retrieved context into a strict prompt template.
   * Forces the local Mistral 7B model to synthesize an answer based *only* on the provided facts, eliminating AI hallucinations.

## 💻 Tech Stack

* **Language:** Python
* **LLM Engine:** Ollama (Mistral 7B, 4-bit Quantized)
* **Embedding Model:** HuggingFace `sentence-transformers`
* **Databases:** FAISS (CPU), SQLite3
* **Libraries:** `requests`, `numpy`, `python-dotenv`

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* [Ollama](https://ollama.com/) installed on your machine.

### 1. Set up the AI Engine
Start your local Ollama server and pull the Mistral model:
```bash
ollama serve
ollama pull mistral
