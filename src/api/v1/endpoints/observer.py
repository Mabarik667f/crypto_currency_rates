from fastapi import APIRouter


router = APIRouter(tags=["observer"], prefix="/obsere")

user_id = 1  # mock object, delete after auth module


@router.get("/description")
async def data_about_observed_coins():
    pass


@router.post("/{coin_id}")
async def observe_coin(coin_id: str):
    pass


@router.delete("/{coin_id}")
async def unobserve_coin(coin_id: str):
    pass


@router.delete("/clean")
async def observe_clean():
    pass
