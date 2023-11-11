import asyncio

import websockets


async def read_messages() -> None:
    HOST = "ip сервиса уведомлений"
    PORT = "port сервиса уведомлений"
    PASSWORD = "пароль сервиса уведомлений"
    uri = fr"ws://{HOST}:{PORT}/notif/{PASSWORD}"

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"{message}")


def main() -> None:
    asyncio.get_event_loop().run_until_complete(read_messages())
