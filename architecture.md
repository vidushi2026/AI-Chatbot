# Groww RAG Chatbot: Architecture Document

## Overview
A phase-wise architecture for a Retrieval-Augmented Generation (RAG) chatbot designed to answer factual queries about mutual fund schemes using Groww's official public pages.

---

## Phase 1: Data Ingestion
**Purpose**: Build an FAQ assistant for mutual fund schemes (expense ratio, exit load, minimum SIP, ELSS lock-in, riskometer, benchmark, statement download).

### Components:
- **Target Sources**: Official Groww public pages (e.g., `https://groww.in/mutual-funds/`).
- **Web Scraper**: Custom scraper using `BeautifulSoup` or `Selenium` configured to:
    - Respect `robots.txt`.
    - Extract tabular data and scheme-specific text.
    - Map every data point to its source URL for strict attribution.
- **Data Validation**: Schema-based validation to ensure all required fields (e.g., Expense Ratio) are captured.

---

## Phase 2: Data Processing and Indexing
**Purpose**: Convert raw scraped data into a searchable knowledge base.

### Components:
- **Text Pre-processing**:
    - Clean HTML tags and boilerplate.
    - Structure data into scheme-specific "Context Blocks".
- **Chunking Strategy**: Semantic chunking or recursive character splitting to preserve context (e.g., keeping "Exit Load" details in one chunk).
- **Embeddings**: Generate vector representations using a modern model (e.g., `text-embedding-3-small` or `all-MiniLM-L6-v2`).
- **Vector Database**: Store embeddings and metadata (source links) in a vector DB like `Pinecone`, `ChromaDB`, or `Milvus`.

---

## Phase 3: Retrieval and Response Generation
**Purpose**: Fetch relevant context and generate grounded, link-attributed answers.

### Components:
- **Retrieval Engine**:
    - **Hybrid Search**: Combine keyword search (BM25) with semantic vector search for better accuracy on scheme names.
    - **Re-ranking**: Post-retrieval re-ranking (e.g., using Cohere Rerank) to select the most relevant chunks.
- **LLM Integration**:
    - **Model**: Groq AI (Llama 3 or Mixtral) for low-latency inference.
    - **Strict Grounding**: The chatbot must **not** answer queries using internal knowledge. It must only use context retrieved from embeddings.
    - **Strict Source Attribution**: **Every answer must include exactly one source link from which the information was derived.**
    - **System Guardrails**: 
        - **Scope**: Answer only factual queries about mutual funds. 
        - **Refuse Out-of-Scope**: Politely decline personal, general, or unrelated questions.
        - **No Financial Advice**: Refuse opinionated/portfolio advice (e.g., "Should I buy/sell?") with a facts-only message and a link to educational content.
        - **No PII**: Strictly prohibit and do not store PII (PAN, Aadhaar, account numbers, OTPs, emails, phone numbers).
- **Response Guardrails**: Verification step to ensure no financial advice is given and the source link is present.

---

## Phase 4: Frontend and Backend Architecture
**Purpose**: Provide a premium interface for users to interact with the chatbot.

### Components:
- **Backend API**:
    - Developed using Python's built-in `http.server` (Zero-dependency).
    - Routes `/api/chat` to the `GrowwChatbot` logic.
- **Frontend UI**:
    - Modern, responsive vanilla HTML/CSS/JS interface.
    - Features: 
        - Chat window with Groww branding.
        - Example questions for **Expense Ratio**, **Min SIP**, and **Exit Load**.
        - Safety disclaimer: "Facts-only. No investment advice."
        - Responses prioritized for brevity ($\le 3$ sentences).
        - Source attribution with "Last updated from sources" footer.

---

## Phase 5: Scheduler Pipeline
**Purpose**: Systematically keep the knowledge base and chatbot responses updated with the latest data from [groww.in](https://groww.in).

### Components:
- **Orchestrator**: Python-based scheduler (`scheduler.py`) running at configurable intervals (e.g., 24 hours).
- **Workflow**:
    1. **Data Ingestion**: Triggers the scraper to collect the latest FAQ and fund data.
    2. **Change Detection**: Generates an MD5 hash of the new dataset and compares it with `data_hash.txt`.
    3. **Automated Processing**: If data has changed, triggers `processor.py` to generate `processed_data.json`.
    4. **Index Update**: Regenerates the `vector_index.json` used by the retrieval layer.
    5. **Metadata Sync**: Updates `last_updated.txt` which is reflected in the Frontend UI.
    6. **Health Check**: Executes `health_check.py` to verify:
        - Index loads correctly.
        - Sample queries return valid, attributed answers.
        - Source link integrity is maintained.
- **Reporting**: Full execution logs are maintained in `scheduler.log`.
---

## Phase 6: Streamlit Deployment (Optional)
**Purpose**: Provide a scalable, easy-to-deploy interface for cloud hosting.

### Components:
- **Application**: `streamlit_app.py` acting as a wrapper for the `GrowwChatbot`.
- **Features**:
    - Custom styled suggestion buttons.
    - Markdown-rendered clickable links.
    - Session state for chat history.
- **Dependencies**: Defined in `requirements.txt`.
