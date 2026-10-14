from fastapi import WebSocket, WebSocketDisconnect
from backend.realtime.event_generator import event_stream
from backend.agents.decision_graph import run_agent
from backend.config import get_settings
from backend.api.schemas import GameSituation
import json
import asyncio

settings = get_settings()

async def realtime_endpoint(websocket: WebSocket):
    await websocket.accept()

    await websocket.send_text(json.dumps({"status": "connected"}))

    try:
        async for event in event_stream(delay=settings.event_delay_seconds):
            situation = GameSituation(**event)

            try:
                result = await asyncio.to_thread(run_agent, situation.to_query())
            except Exception as exc:
                await websocket.send_text(json.dumps({
                    "event": event,
                    "error": {
                        "message": "Agent inference failed",
                        "detail": str(exc),
                    },
                }))
                continue

            payload = {
                "event": event,
                "decision": result.get("decision"),
                "critique": result.get("critique"),
                "evidence": result.get("evidence", []),
            }

            await websocket.send_text(json.dumps(payload))

    except WebSocketDisconnect:
        print("Client disconnected from realtime stream")
