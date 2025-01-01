from loguru import logger
from fastapi import Response, Request


async def log_middleware(request: Request, call_next) -> Response:
    response = await call_next(request)
    logger.debug(f"{request.method} {request.url} {response.status_code}")
    return response
