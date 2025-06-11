# 🛠 Technical Approach – University FAQ Chatbot (RAG) – Altibbe AI Intern Task

This document outlines the architecture, rationale, workflow design, and implementation details of a Retrieval-Augmented Generation (RAG) chatbot developed using **n8n**, **Google Gemini**, and **Pinecone**. The bot assists students by answering university-related queries using a document-based FAQ system.

---

## 📐 Architecture Overview

The solution is divided into **two separate workflows** in n8n:

### 1. **Data Ingestion & Indexing Workflow**
This workflow is triggered whenever a new FAQ document (PDF) is uploaded to a specific **Google Drive folder**. It processes the document, generates semantic embeddings using **Google Gemini**, and stores them in **Pinecone** for future retrieval.

### 2. **Chatbot Interaction Workflow**
This workflow receives incoming user questions via a webhook, semantically searches the vector store for relevant FAQ context, and uses **Google Gemini's chat model** to generate accurate and context-aware responses.

---

## 🔄 Workflow 1: Document Processing & Vector Insertion

### 📌 Purpose:
Automatically process new FAQ documents and store semantically indexed chunks into Pinecone.

### 🧱 Nodes Used:
1. **Google Drive Trigger** – Watches a folder for new file uploads.
2. **Google Drive** – Downloads the new file (PDF).
3. **Default Data Loader** – Converts the binary PDF into text.
4. **Recursive Character Text Splitter** – Splits text into ~500-character chunks.
5. **Embeddings Google Gemini** – Generates vector embeddings for each chunk.
6. **Pinecone Vector Store** – Upserts each chunk (with metadata) into the `n8n-gemini` Pinecone index.

### 📌 Strategy:
- Documents are split into manageable semantic units using recursive character splitting.
- Embeddings are generated using **Google Gemini's embedding model (`models/embedding-001`)**.
- Chunks are stored with metadata (`text`) in **Pinecone**, enabling fast and relevant retrieval during chat interaction.

---

## 💬 Workflow 2: Chatbot Interaction via Webhook

### 📌 Purpose:
Receive user queries and respond with fact-based, semantically relevant answers using the indexed FAQ data.

### 🧱 Nodes Used:
1. **Chat Trigger (Webhook)** – Receives incoming questions via HTTP POST.
2. **AI Agent** – Central node that routes the query, context, and tools to an LLM agent.
3. **Simple Memory** – Maintains recent conversation history for coherence.
4. **Answer Questions with Vector Store (Tool)** – Uses similarity search to pull relevant FAQ chunks from Pinecone.
5. **Pinecone Vector Store** – Retrieves matching chunks based on query embedding.
6. **Embeddings Google Gemini** – Converts the user's query into a vector.
7. **Google Gemini Chat Model** – Generates the final response using the retrieved context and query.

### 🧠 System Prompt:
A detailed system message guides the agent to:
- Use only provided context
- Avoid speculation or external knowledge
- Maintain a helpful, empathetic, and student-focused tone

### 🔍 Retrieval Details:
- Top-K similarity search returns the most relevant FAQ chunks
- Chunks are embedded using **Gemini Embeddings**
- Matching scores are transparent for traceability

---

## 📈 Performance Considerations

- **Chunk Size (500 tokens)**: Balances retrieval granularity and semantic coherence.
- **Low LLM temperature (0.3)**: Ensures factual and stable outputs.
- **Embeddings and LLM model kept consistent** (both Gemini): Avoids cross-model embedding drift.

---

## 🧠 Design Rationale

| Decision | Reason |
|---------|--------|
| Split workflows | Keeps ingestion decoupled from query answering. Allows real-time updates without restarting chatbot logic. |
| Google Drive Trigger | Enables dynamic document updates without manual file handling. |
| Google Gemini | Cost-effective and fast embeddings + LLM generation with Google API |
| Pinecone | Scalable, fast vector database with simple API integration |
| Memory Node | Allows multi-turn chat and context awareness |
| Modular n8n Design | Enhances maintainability, debugging, and visual flow |

---

## 🧩 Challenges Faced

| Challenge | Solution |
|----------|----------|
| No native Gemini embedding in Python | Used n8n node-based embedding |
| Gemini dimension uncertainty | Confirmed vector size compatibility with Pinecone |
| Context formatting for LLM | Designed clear, consistent prompt template with retrieved chunks |
| Workflow bloat | Split into two clean, maintainable workflows |

---

## 🚀 Future Improvements

- Enable **real-time vector upsert** from UI uploads (no Google Drive dependency)
- Add **query analytics dashboard** for tracking frequent student questions
- Integrate **Slack or Discord webhook** for conversational access
- Implement **response caching** to reduce repeat token usage
- Expand to **multi-modal support** (e.g., images or tables in documents)

---

## ✅ Summary

This project demonstrates a fully working and ethical implementation of a student-facing FAQ chatbot using modern AI tools, vector search, and no-code automation. It is accurate, modular, and aligned with the values of responsible AI development.

