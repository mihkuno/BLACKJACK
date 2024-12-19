from fastapi import FastAPI
from starlette.responses import FileResponse 
from starlette.websockets import WebSocket

from service.vision import detect, from_b64

app = FastAPI()

@app.get("/test")
async def test_endpoint():
    return {"message": "Test is working!"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        img = await websocket.receive_text()
        await websocket.send_text( detect(img) )