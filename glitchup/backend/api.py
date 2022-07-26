import asyncio

import aioredis
import uvloop
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config
from rq import Queue

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
redis_conn, redis_queue = None, None


@app.on_event("startup")
async def setup() -> None:
    """Setup necessities for the API, like Redis (database) connection and Redis queue."""
    global redis_queue, redis_conn
    redis_conn = aioredis.from_url("redis://redis:6379")
    redis_queue = Queue(connection=redis_conn)


@app.get("/")
async def root() -> FileResponse:
    """Return the root page."""
    return FileResponse("../frontend/static/index.html")


@app.websocket("/ws")
async def temp_ws_endpoint(ws: WebSocket) -> None:
    """Only here temporarily so I can commit without pre-commit complaining about not using the WebSocket import"""
    ...


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(serve(app, Config()))  # type: ignore
