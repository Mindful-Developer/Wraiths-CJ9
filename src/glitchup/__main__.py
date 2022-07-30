import asyncio
from pathlib import Path
from typing import Type
from ast import literal_eval

# import httpx
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config
from pydantic import BaseModel
from web.filters.dotted import Dotted # type: ignore
from web.filters.ghosting import Ghosting  # type: ignore
from web.filters.image_filter import ImageFilter  # type: ignore
from web.filters.number import Number  # type: ignore
from web.filters.metaldot import MetalDot  # type: ignore
from web.filters.parameter import Parameter  # type: ignore
from web.worker import redis_conn, redis_queue  # type: ignore

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=Path(BASE_DIR, "web/static")), name="static")
FILTERS = {
    "981": Dotted,
    "982": Ghosting,
    "983": Number,
    "984": MetalDot,
}


@app.on_event("startup")
async def setup() -> None:
    """Configure and set a few things on app startup."""
    await redis_conn.rpush(
        "filters",
        str(
            {
                "id": Ghosting.filter_id,
                "name": "Ghosting",
                "description": Ghosting.__doc__,
                "inputs": Ghosting.metadata()[0],
                "parameters": ", ".join(repr(p) for p in Ghosting.metadata()[1]),
            }
        ),
        str(
            {
                "id": Dotted.filter_id,
                "name": "Dotted",
                "description": Dotted.__doc__,
                "inputs": Dotted.metadata()[0],
                "parameters": ", ".join(repr(p) for p in Dotted.metadata()[1]),
            }
        ),
        str(
            {
                "id": Number.filter_id,
                "name": "Number",
                "description": Number.__doc__,
                "inputs": Number.metadata()[0],
                "parameters": ", ".join(repr(p) for p in Number.metadata()[1]),
            }
        ),
        str(
            {
                "id": MetalDot.filter_id,
                "name": "MetalDot",
                "description": MetalDot.__doc__,
                "inputs": MetalDot.metadata()[0],
                "parameters": ", ".join(repr(p) for p in MetalDot.metadata()[1]),
            }
        ),
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
        content=filter_class.to_json(),
        )



@app.post("/filters/create/")
async def create_filter(filter_metadata: FilterMetadata) -> Type[ImageFilter]:
    """Create a new filter."""
    filter_cls = type(f"{filter_metadata.name}", (ImageFilter,), {})
    filter_cls.__doc__ = filter_metadata.description
    setattr(filter_cls, "filter_id", filter_metadata.filter_id)

    await redis_conn.rpush(
        "filters",
        str(
            {
                "id": filter_metadata.filter_id,
                "name": filter_metadata.name,
                "description": filter_metadata.description,
                "inputs": filter_metadata.inputs,
                "parameters": filter_metadata.parameters,
            }
        ),
    )

    return filter_cls


@app.websocket("/image/apply-filter/{filter_id}")
async def apply_filter(filter_id: int, ws: WebSocket) -> None:
    """Apply a filter to an image."""
    ...


if __name__ == "__main__":
    asyncio.run(serve(app, Config()))  # type: ignore
