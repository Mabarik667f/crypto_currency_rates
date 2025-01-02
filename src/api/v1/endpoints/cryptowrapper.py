from core.deps import MongoDep
from cryptowrapper.services import BaseCoinsSet, coins_market
from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from loguru import logger

router = APIRouter(tags=["cryptowrapper"], prefix="/cryptowrapper")


@router.post("/coins")
async def set_coins(db: MongoDep):
    coins = await BaseCoinsSet(db).set_coins()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"coins": coins})


@router.put("/coins")
async def all_data_about_coins(db: MongoDep, coins_ids: list[str]):
    coins_data = await coins_market()
