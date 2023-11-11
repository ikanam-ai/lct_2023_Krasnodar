import asyncio

from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks

from .config import PORT, NOTIF_PSWD, ADMIN_PSWD
from .models.event import Event
from .models.message import Message

app = FastAPI()

websockets: set[WebSocket] = set()


async def send_event(event: Event) -> None:
    for socket in websockets:
        await socket.send_json(event.model_dump_json())


@app.websocket("/notif/{key}")
async def websocket_endpoint(key: str, websocket: WebSocket):
    await websocket.accept()
    if key != NOTIF_PSWD:
        return await websocket.close()
    try:
        websockets.add(websocket)
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        websockets.remove(websocket)


@app.post("/accept")
async def accept_message(message: Message, background_tasks: BackgroundTasks) -> None:
    if message.pswd != ADMIN_PSWD:
        raise HTTPException(status_code=404, detail="Not found")
    background_tasks.add_task(send_event, message.event)


def main() -> None:
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=False)
