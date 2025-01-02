from typing import Annotated
from fastapi import Request, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase


async def get_db(request: Request) -> AsyncIOMotorDatabase:
    return request.app.db


MongoDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]
