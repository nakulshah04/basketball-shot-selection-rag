import asyncio
import os

import pytest
import websockets


pytestmark = pytest.mark.integration


async def receive_messages(limit=5):
    uri = "ws://127.0.0.1:8000/ws/realtime"
    async with websockets.connect(
        uri,
        open_timeout=20,
        ping_interval=None,
    ) as websocket:

        messages = []
        for _ in range(limit):
            msg = await websocket.recv()
            messages.append(msg)
        return messages


@pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Requires the FastAPI websocket server.",
)
def test_realtime_websocket_smoke():
    messages = asyncio.run(receive_messages())

    assert messages


if __name__ == "__main__":
    messages = asyncio.run(receive_messages())

    for index, msg in enumerate(messages, start=1):
        print(f"\nEVENT {index}:")
        print(msg)
