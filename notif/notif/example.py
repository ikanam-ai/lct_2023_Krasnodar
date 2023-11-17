import asyncio
import websockets
from .config import PORT, NOTIF_PSWD


async def read_messages():
    uri = fr"ws://localhost:{PORT}/notif/{NOTIF_PSWD}"

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"{message}")


def main() -> None:
    asyncio.get_event_loop().run_until_complete(read_messages())
