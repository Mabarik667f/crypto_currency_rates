from fastapi import APIRouter


router = APIRouter(tags=["observer"], prefix="/obsere")


@router.get("/description")
async def data_about_observed_coins():
    pass


@router.post("/{coin_id}")
async def set_observe_coin_data():
    pass


@router.delete("/{coin_id}")
async def unset_observe_coin_data():
    pass


@router.delete("/clean")
async def observe_clean():
    pass
