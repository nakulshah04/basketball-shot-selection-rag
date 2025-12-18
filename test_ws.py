import asyncio
import websockets

async def test():
    uri = "ws://127.0.0.1:8000/ws/realtime"
    async with websockets.connect(
        uri,
        open_timeout=20,
        ping_interval=None,
    ) as websocket:

        for i in range(5):
            msg = await websocket.recv()
            print(f"\nEVENT {i+1}:")
            print(msg)

asyncio.run(test())