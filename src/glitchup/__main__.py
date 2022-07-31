#!/usr/bin/env python3

import asyncio
import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Form, UploadFile, WebSocket
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
from web.models import UploadedImage
from web.worker import Worker, redis_conn, redis_queue  # type: ignore

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=Path(BASE_DIR, "web/static")), name="static")


@app.on_event("startup")
async def setup() -> None:
    """Add filters to database."""
    redis_conn.sadd(
        "filters",
        str(Ghosting.to_dict()),
        str(Dotted.to_dict()),
        str(Number.to_dict()),
        str(MetalDot.to_dict()),
        str(PixelSort.to_dict()),
    )


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


@app.get("/filters/filter/{filter_id}")
async def get_filter(filter_id: int) -> JSONResponse:
    """Get a filter by ID."""
    filters = redis_conn.smembers("filters")

    for f in filters:
        f = json.loads(f.translate(f.maketrans("'()", '"[]')))

        if f["filter_id"] == filter_id:
            return JSONResponse(
                content=f,
                status_code=200,
            )
        else:
            continue

    return JSONResponse(
        content={"error": "Filter not found."},
        status_code=404,
    )


@app.post("/images/upload")
async def upload_image(image: UploadFile) -> JSONResponse:
    """Upload an image to the server."""
    image_path = Path(BASE_DIR, "web/static/uploads/") / image.filename
    image_path.write_bytes(await image.read())

    uploaded_image = UploadedImage(path=image_path.as_posix())

    redis_conn.sadd("images", str(uploaded_image.to_dict()))

    return JSONResponse(
        content=uploaded_image.to_dict(),
        status_code=200,
    )


@app.post("/images/add")
async def add_image(
    image_id: int = Form(), filter_id: int = Form(), *params: Any
) -> int:
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
    """Get an image by ID."""
    ...


asyncio.run(serve(app, Config()))  # type: ignore
