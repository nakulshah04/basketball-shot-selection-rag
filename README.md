# Basketball Shot Selection Coach

I built this as an experiment in making an LLM useful during a basketball
possession instead of merely conversational. Given a live game situation, it
retrieves comparable recorded attempts, recommends a shot type, and shows the
evidence behind that recommendation in a local dashboard.

This is a portfolio prototype, not a coaching system. A good recommendation is
only as good as the available shot data: it does not see a game, understand a
playbook, or replace a coach's judgment.

## Architecture

- **RAG**: Local Ollama embeddings + Chroma, with source IDs retained as evidence
- **Agents**: LangGraph (Decision + Critic with retries)
- **LLM**: Local (Ollama) for zero-API dependency
- **Realtime**: FastAPI WebSockets
- **Frontend**: React + TypeScript (live dashboard)

## Data, honestly

For a real corpus, use the first-party NBA Stats shot-chart endpoint via the
included downloader; it creates a local, versioned CSV snapshot rather than
calling NBA Stats while the app runs. The existing `shot_data.csv` is synthetic
and is only a development fixture. See [the data notes](backend/data/README.md)
before presenting results as historical analysis.

## Run

```bash
# backend setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# build or refresh the retrieval corpus/vector store
python -m backend.rag.build_corpus
python -m backend.rag.embeddings

# start local model and API
ollama serve
uvicorn backend.app:app

# frontend
cd frontend
npm install
npm run dev
```

Before building embeddings, download the local Ollama embedding model:

```bash
ollama pull nomic-embed-text
```

## Configuration

Runtime defaults live in `.env.example` and can be overridden in `.env`.

- `OLLAMA_MODEL`: local chat model used by the decision and critic agents.
- `OLLAMA_TEMPERATURE`: generation temperature. Keep this low for repeatable decisions.
- `RETRIEVER_K`: number of retrieved shot examples passed into the decision prompt.
- `MAX_AGENT_RETRIES`: maximum self-correction attempts after an invalid critique.
- `EVENT_DELAY_SECONDS`: delay between simulated realtime events.
- `VITE_WS_URL`: optional frontend websocket URL override.

## Quality Checks

```bash
pytest

cd frontend
npm run build
npm run lint
```

## Improvement Plan

Completed in this pass:

- Parse model responses into structured decision and critique objects, including fenced or extra-text JSON.
- Add a bounded LangGraph retry loop so critic rejection cannot produce an infinite correction cycle.
- Centralize backend settings for model, embeddings, retriever depth, vector store path, and stream timing.
- Keep the realtime websocket alive when a single agent inference fails by sending structured error payloads.
- Add focused backend tests for JSON parsing and retry behavior.
- Replace the starter frontend with a typed, responsive live dashboard that exposes connection and stream errors.

Recommended next steps:

- Add an offline evaluation mode with mocked LLM outputs so CI can measure retrieval and validation behavior without Ollama.
- Include metadata in Chroma documents, then retrieve/filter by location, shot clock bucket, and defender distance.
- Add a small API endpoint for one-off decisions so the system is testable without opening a websocket stream.
- Record evaluation runs to JSON or CSV to compare prompt/model changes over time.

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
