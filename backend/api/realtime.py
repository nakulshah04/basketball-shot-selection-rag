from fastapi import WebSocket, WebSocketDisconnect
from backend.realtime.event_generator import event_stream
from backend.agents.decision_graph import run_agent
from backend.config import get_settings
import json
import asyncio

settings = get_settings()

async def realtime_endpoint(websocket: WebSocket):
    await websocket.accept()

    await websocket.send_text(json.dumps({"status": "connected"}))

    try:
        async for event in event_stream(delay=settings.event_delay_seconds):
            query = (
                f"{event['time_remaining']} seconds left, "
                f"score difference {event['score_diff']}, "
                f"defender {event['defender_distance']} meters away at {event['location']}"
            )

            try:
                result = await asyncio.to_thread(run_agent, query)
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
                "critique": result.get("critique")
            }

            await websocket.send_text(json.dumps(payload))

    except WebSocketDisconnect:
        print("Client disconnected from realtime stream")
