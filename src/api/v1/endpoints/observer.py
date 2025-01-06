import aiohttp
from datetime import timedelta
from core import settings
from fastapi import APIRouter, status
from observer.deps import ObserverServDep
from cryptowrapper.schemas import BaseCoin, DescribedCoin
from observer.schemas import AddObserveCoins
from loguru import logger

router = APIRouter(tags=["observer"], prefix="/observer")


@router.delete("/coins/clear", status_code=status.HTTP_204_NO_CONTENT)
async def observe_clear(service: ObserverServDep):
    await service.clear_observer()


@router.get("/coins")
async def get_observed_coins(
    service: ObserverServDep,
) -> list[BaseCoin]:
    return await service.get_observed_coins()


@router.put("/coins/delete")
async def del_observed_coins(
    coins_ids: AddObserveCoins,
    service: ObserverServDep,
) -> list[BaseCoin]:
    observed_coins = await service.del_observe_for_coins(coins_ids.coins_ids)
    return observed_coins


@router.put("/coins/add")
async def add_observed_coins(
    coins_ids: AddObserveCoins,
    service: ObserverServDep,
) -> list[BaseCoin]:
    observed_coins = await service.add_observe_for_coins(coins_ids.coins_ids)
    return observed_coins


@router.get("/coins/describe")
async def get_describe_obsreved_coins(
    service: ObserverServDep,
) -> list[DescribedCoin]:
    described_coins = await service.get_describe_observed_coins()
    return described_coins
