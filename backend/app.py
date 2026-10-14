import asyncio

from fastapi import FastAPI, WebSocket

from backend.agents.decision_graph import run_agent
from backend.api.realtime import realtime_endpoint
from backend.api.schemas import DecisionResponse, GameSituation

app = FastAPI(title="Agentic Shot Selection")

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/decisions", response_model=DecisionResponse)
async def make_decision(situation: GameSituation):
    result = await asyncio.to_thread(run_agent, situation.to_query())
    return {
        "situation": situation,
        "decision": result["decision"],
        "critique": result["critique"],
        "evidence": result["evidence"],
    }

@app.websocket("/ws/realtime")
async def realtime_ws(websocket: WebSocket):
    await realtime_endpoint(websocket)
