import asyncio
import websockets


async def read_messages():
    uri = "ws://localhost:8094/notif/HELLO"

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"{message}")


def main() -> None:
    asyncio.get_event_loop().run_until_complete(read_messages())
