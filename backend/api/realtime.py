from fastapi import WebSocket, WebSocketDisconnect
from backend.realtime.event_generator import event_stream
from backend.agents.decision_graph import run_agent
import json
import asyncio

async def realtime_endpoint(websocket: WebSocket):
    await websocket.accept()

    # 🔑 Immediately acknowledge connection
    await websocket.send_text(json.dumps({"status": "connected"}))

    try:
        async for event in event_stream():
            query = (
                f"{event['time_remaining']} seconds left, "
                f"score difference {event['score_diff']}, "
                f"defender {event['defender_distance']} meters away at {event['location']}"
            )

            # 🔑 Run blocking agent code in a thread
            result = await asyncio.to_thread(run_agent, query)

            payload = {
                "event": event,
                "decision": result.get("decision"),
                "critique": result.get("critique")
            }

            await websocket.send_text(json.dumps(payload))

    except WebSocketDisconnect:
        print("Client disconnected from realtime stream")