import aioredis
from fastapi import FastAPI, WebSocket
from rq import Queue

app = FastAPI()
redis_conn, redis_queue = None, None


@app.on_event("startup")
async def setup() -> None:
    """Setup necessities for the API, like Redis (database) connection and Redis queue."""
    global redis_queue, redis_conn
    redis_conn = aioredis.from_url("redis://redis:6379")
    redis_queue = Queue(connection=redis_conn)


@app.get("/")
async def root() -> dict[str, str]:
    """Root route."""
    return {"message": "Hello World"}


@app.websocket("/ws")
async def temp_ws_endpoint(ws: WebSocket) -> None:
    """Only here temporarily so I can commit without pre-commit complaining about not using the WebSocket import"""
    ...
