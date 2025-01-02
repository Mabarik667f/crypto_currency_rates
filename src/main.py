from core.exceptions import BaseError
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from core import init_db, logger, log_middleware, settings  # flake8: noqa
from api import api_router


@asynccontextmanager
async def mongo_lifespan(app: FastAPI):
    client, db = await init_db()
    app.client = client  # type: ignore[attr-defined]
    app.db = db  # type: ignore[attr-defined]
    yield
    client.close()  # type: ignore[attr-defined]


app = FastAPI(lifespan=mongo_lifespan)
app.include_router(api_router)


@app.middleware("http")
async def log_middleware_wrapper(request: Request, call_next):
    return await log_middleware(request, call_next)


@app.exception_handler(BaseError)
def core_validation_exc_handler(request: Request, exc: BaseError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.to_dict()}
    )
