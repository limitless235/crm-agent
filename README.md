# AntiGravity AI Support System

A high-performance, asynchronous AI Support System featuring a FastAPI backend, Redis-stream based AI processing with RAG, a Next.js frontend, and DuckDB analytics.

## System Architecture

- **Frontend**: Next.js (App Router, Tailwind CSS, WebSockets).
- **Backend API**: FastAPI (REST endpoints, JWT Auth, Redis Stream Publisher).
- **AI Worker**: Python service using `llama-cpp-python` for local inference and `SentenceTransformers` for RAG.
- **Vector Store**: ChromaDB (Source of Truth) + FAISS (Derived Index).
- **Message Broker**: Redis Streams (Asynchronous task queue).
- **Database**: PostgreSQL (Transactional data).
- **Analytics**: DuckDB (OLAP queries on periodic ingestion).

## Prerequisites

- Docker and Docker Compose.
- A GGUF LLM model (e.g., Llama-2-7B-Chat or Mistral-7B).

## Setup & Running

1. **Clone and Configure**:
   - Ensure you have a `.env` file in the root with valid credentials (see `.env.example`).
   - Place your LLM model (GGUF) at `ai_worker/data/models/model.gguf`.

2. **Run with Docker Compose**:
   ```bash
   docker compose up --build
   ```

3. **Access the System**:
   - **Frontend**: `http://localhost:3000`
   - **API Docs**: `http://localhost:8001/api/v1/docs` (Container maps 8000 to 8001)

## Components Detail

### AI Worker (Phase 9.4 Hardened)
- Uses Redis Streams for decoupled, asynchronous processing.
- Implements RAG with semantic search via FAISS.
- Production-hardened with poison-message protection, idempotency, and graceful degradation.

### Backend Worker
- Consumes AI responses from Redis and persists them to Postgres.
- Notifies the frontend via Redis PubSub for real-time WebSocket updates.

### Analytics
- DuckDB based engine that ingests data from Postgres for lightning-fast OLAP queries.

## Testing

Run end-to-end tests:
```bash
pip install -r tests/requirements.txt
pytest tests/e2e/test_system.py
```

## Security Model
- JWT based authentication with short-lived tokens.
- Mandatory JWT validation for WebSockets.
- Rate limiting on all API endpoints.
- Input sanitization via `bleach`.
