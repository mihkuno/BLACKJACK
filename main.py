from fastapi import FastAPI
from starlette.responses import FileResponse 
from starlette.websockets import WebSocket

from service.visual_manipulation import detect, from_b64

app = FastAPI()

@app.get("/")
async def index_endpoint():
    return FileResponse('client/index.html')


@app.get("/hello")
async def test_endpoint():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        img = await websocket.receive_text()
        await websocket.send_text( detect(img) )