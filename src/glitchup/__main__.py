#!/usr/bin/env python3

import asyncio
from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config
from rq.command import send_shutdown_command
from web.filters.builtin.dotted import Dotted  # type: ignore
from web.filters.builtin.ghosting import Ghosting  # type: ignore
from web.filters.builtin.metaldot import MetalDot  # type: ignore
from web.filters.builtin.number import Number  # type: ignore
from web.filters.builtin.pixelsort import PixelSort  # type: ignore
from web.filters.image_filter import ImageFilter  # type: ignore
from web.filters.parameter import Parameter  # type: ignore
from web.models import FilterMetadata  # type: ignore
from web.worker import Worker, redis_conn, redis_queue  # type: ignore

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=Path(BASE_DIR, "web/static")), name="static")
FILTERS = {
    "981": Dotted,
    "982": Ghosting,
    "983": Number,
    "984": MetalDot,
    "985": PixelSort,
}


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown the web server and connections to database."""
    for worker in Worker.all(queue=redis_queue):
        send_shutdown_command(redis_conn, worker.name)
        worker.close()

    redis_queue.delete()
    redis_conn.close()


@app.get("/")
async def root() -> FileResponse:
    """Return the root page."""
    return FileResponse(f"{BASE_DIR}/web/static/index.html")


@app.get("/filters/{filter_id}")
async def get_filter(filter_id: str) -> JSONResponse:
    """Get a filter by ID."""
    if filter_id not in FILTERS:
        return JSONResponse(
            status_code=404,
            content={"message": f"Filter {filter_id} not found."},
        )

    filter_class = FILTERS[filter_id]
    return JSONResponse(
        status_code=200,
        content=filter_class.to_dict(),
    )


@app.post("/images/add")
async def add_image() -> int:
    """Upload an image to the server."""
    ...


@app.websocket("/images/{image_id}/apply/{filter_id}")
async def apply_filter_to_image(ws: WebSocket, image_id: int, filter_id: int) -> None:
    """Apply a filter to an image."""
    await ws.accept()
    # worker = Worker()

    ...


@app.websocket("/images/{image_id}")
async def get_image(image_id: str, ws: WebSocket) -> None:
    ...


asyncio.run(serve(app, Config()))  # type: ignore
