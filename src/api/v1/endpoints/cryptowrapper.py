from core.deps import MongoDep
from cryptowrapper.schemas import BaseCoin
from cryptowrapper.services import BaseCoinsSet
from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from loguru import logger
from cryptowrapper.crud import get_coins_by_query

router = APIRouter(tags=["cryptowrapper"], prefix="/cryptowrapper")


@router.post("/coins")
async def set_coins(db: MongoDep):
    coins = await BaseCoinsSet(db).set_coins()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"coins": coins})


@router.get("/search-coins")
async def get_coins(db: MongoDep, limit: int = 5, query: str = "") -> list[BaseCoin]:
    coins = await get_coins_by_query(db, query, limit=limit)
    return coins
