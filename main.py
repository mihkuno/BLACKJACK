from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

from service.visual_manipulation import detect, from_b64

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        img = await websocket.receive_text()
        await websocket.send_text( detect(img) )