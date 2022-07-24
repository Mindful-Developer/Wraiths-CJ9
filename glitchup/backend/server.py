# import aioredis
from fastapi import FastAPI

from .redis import Redis

# from rq import Queue


app = FastAPI()
redis = Redis.get_connection()


# @app.on_event("startup")
# async def setup() -> None:
#     """Setup Redis and other things on app startup"""
#     redis_queue = Queue(connection=redis)


@app.get("/")
async def root() -> dict[str, str]:
    """Root route."""
    return {"message": "Hello World"}
