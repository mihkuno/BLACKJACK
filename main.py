from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from service.visual_manipulation import detect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text( detect(data) )