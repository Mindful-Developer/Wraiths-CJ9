# import httpx
import asyncio
from typing import Type

import aioredis
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config
from pydantic import BaseModel
from rq import Queue

from ..filters.dotted import Dotted
from ..filters.ghosting import Ghosting
from ..filters.image_filter import ImageFilter
from ..filters.parameter import Parameter

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
redis_conn, redis_queue = None, None


@app.on_event("startup")
async def setup() -> None:
    """Setup necessities for the API, like Redis (database) connection and Redis queue."""
    global redis_queue, redis_conn
    redis_conn = aioredis.from_url("redis://redis:6379")
    redis_queue = Queue(connection=redis_conn)

    await redis_conn.hset(
        "filters",
        mapping={
            "id": Ghosting.filter_id,
            "name": "Ghosting",
            "description": Ghosting.__doc__,
            "inputs": Ghosting.metadata()[0],
            "parameters": Ghosting.metadata()[1],
        },
    )
    await redis_conn.hset(
        "filters",
        mapping={
            "id": Dotted.filter_id,
            "name": "Dotted",
            "description": Dotted.__doc__,
            "inputs": Dotted.metadata()[0],
            "parameters": Dotted.metadata()[1],
        },
    )


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown the web server and connections to database."""
    global redis_conn, redis_queue

    if redis_conn is not None and redis_queue is not None:
        redis_queue.delete()
        await redis_conn.close()


@app.get("/")
async def root() -> FileResponse:
    """Return the root page."""
    return FileResponse("../frontend/static/index.html")


class FilterMetadata(BaseModel):
    """Metadata for a filter."""

    filter_id: int
    name: str
    description: str
    inputs: int
    parameters: list[Parameter]


@app.get("/filters/filter/{filter_id}")
async def get_filter(filter_id: int) -> Type[ImageFilter]:
    """Get a filter by ID."""
    ...


@app.post("/filters/create/")
async def create_filter(filter_metadata: FilterMetadata) -> Type[ImageFilter]:
    """Create a new filter."""
    filter_cls = type(f"{filter_metadata.name}", (ImageFilter,), {})
    filter_cls.__doc__ = filter_metadata.description
    setattr(filter_cls, "filter_id", filter_metadata.filter_id)

    if redis_conn is not None:
        await redis_conn.hset(
            "filters",
            mapping={
                "id": filter_metadata.filter_id,
                "name": filter_metadata.name,
                "description": filter_metadata.description,
                "inputs": filter_metadata.inputs,
                "parameters": filter_metadata.parameters,
            },
        )

    return filter_cls


@app.websocket("/image/apply-filter/{filter_id}")
async def apply_filter(filter_id: int, ws: WebSocket) -> None:
    """Apply a filter to an image."""
    ...


if __name__ == "__main__":
    asyncio.run(serve(app, Config()))  # type: ignore
