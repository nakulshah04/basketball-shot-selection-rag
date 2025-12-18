from fastapi import FastAPI, WebSocket
from backend.api.realtime import realtime_endpoint

app = FastAPI(title="Agentic Shot Selection")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.websocket("/ws/realtime")
async def realtime_ws(websocket: WebSocket):
    await realtime_endpoint(websocket)