import aiohttp
from core.deps import MongoDep
from fastapi.routing import APIRouter
from core import settings
from loguru import logger

router = APIRouter(tags=["cryptowrapper"], prefix="/cryptowrapper")


@router.post('/coins')
async def set_new_data_about_coins(db: MongoDep):
    async with aiohttp.ClientSession() as session:
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": settings.COIN_GECKO_API_KEY
        }
        async with session.get("https://api.coingecko.com/api/v3/coins/list", headers=headers) as r:
            body = await r.json()
            logger.info(body)



@router.put("/coins")
async def update_all_coins_data(db: MongoDep):
    pass
