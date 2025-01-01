from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from core import init_db, logger, log_middleware


@asynccontextmanager
async def mongo_lifespan(app: FastAPI):
    client, db = await init_db()
    app.client = client  # type: ignore[attr-defined]
    app.db = db  # type: ignore[attr-defined]
    yield
    client.close()  # type: ignore[attr-defined]


app = FastAPI(lifespan=mongo_lifespan)


@app.middleware("http")
async def log_middleware_wrapper(request: Request, call_next):
    return await log_middleware(request, call_next)
