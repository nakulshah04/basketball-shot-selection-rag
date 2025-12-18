# Agentic Shot Selection (RAG + LangGraph)

An end-to-end agentic AI system that streams live game states, retrieves historical context, makes decisions, and self-critiques in real time.

## Architecture

- **RAG**: Local embeddings (SentenceTransformers) + Chroma
- **Agents**: LangGraph (Decision + Critic with retries)
- **LLM**: Local (Ollama) for zero-API dependency
- **Realtime**: FastAPI WebSockets
- **Frontend**: React + TypeScript (live dashboard)

## Run

```bash
# backend
ollama serve
uvicorn backend.app:app

# frontend
cd frontend
npm run dev
```

## Why was this project interesting for me?

Most LLM demos stop at single-prompt responses with no grounding, validation, or system-level behavior.  
This project goes further by building a **fully agentic, end-to-end decision system**.

Key aspects that make it interesting:

- **Agentic control flow**: Uses LangGraph to orchestrate a decision agent and a critic agent, enabling self-correction when decisions are not grounded in retrieved evidence.
- **Retrieval-grounded reasoning**: Implements a RAG pipeline with local embeddings and a vector database to ensure decisions are based on historical context rather than hallucinated patterns.
- **Real-time inference**: Streams simulated live game states over WebSockets and performs on-the-fly retrieval, reasoning, and validation for each event.
- **Production-style design**: Separates data ingestion, retrieval, agent logic, evaluation, and presentation layers, mirroring real-world AI system architecture.
- **Zero external API dependency**: Runs entirely on local models, making the system reproducible, cost-free, and robust to rate limits.

The result is a system that behaves more like an intelligent service than a chatbot, emphasizing reliability, grounding, and continuous decision-making.
