from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def setup_redis() -> None:
    """Setup the redis server for the application."""
    pass


@app.get("/")
async def root() -> dict[str, str]:
    """Root route."""
    return {"message": "Hello World"}
