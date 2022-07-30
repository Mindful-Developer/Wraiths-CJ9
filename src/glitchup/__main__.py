import asyncio
from pathlib import Path
from typing import Type

# import httpx
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config
from pydantic import BaseModel
from web.filters.builtin.dotted import Dotted  # type: ignore
from web.filters.builtin.ghosting import Ghosting  # type: ignore
from web.filters.builtin.metaldot import MetalDot  # type: ignore
from web.filters.builtin.number import Number  # type: ignore
from web.filters.image_filter import ImageFilter  # type: ignore
from web.filters.parameter import Parameter  # type: ignore
from web.worker import redis_conn, redis_queue  # type: ignore

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=Path(BASE_DIR, "web/static")), name="static")


@app.on_event("startup")
async def setup() -> None:
    """Configure and set a few things on app startup."""
    await redis_conn.sadd(
        "filters",
        str(Ghosting.to_dict()),
        str(Dotted.to_dict()),
        str(Number.to_dict()),
        str(MetalDot.to_dict()),
    )


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown the web server and connections to database."""
    redis_queue.delete()
    await redis_conn.close()


@app.get("/")
async def root() -> FileResponse:
    """Return the root page."""
    return FileResponse(f"{BASE_DIR}/web/static/index.html")


class FilterMetadata(BaseModel):
    """Metadata for a filter."""

    filter_id: int
    name: str
    description: str
    inputs: int
    parameters: list[Parameter]

    class Config:
        arbitrary_types_allowed = True


@app.get("/filters")
async def get_all_filters() -> list[FilterMetadata]:
    """Return all filters."""
    ...


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

    await redis_conn.sadd(
        "filters",
        str(filter_cls.to_dict()),  # type: ignore
    )

    return filter_cls


@app.websocket("/image/apply-filter/{filter_id}")
async def apply_filter(filter_id: int, ws: WebSocket) -> None:
    """Apply a filter to an image."""
    ...


asyncio.run(serve(app, Config()))  # type: ignore
