from accounts.schemas import MongoBaseUser
from auth.schemas import TokenData
from cryptowrapper.schemas import BaseCoin
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from observer.crud import ObserverCrud
from observer.services import ObserverService
from loguru import logger

# async def test_set_observed_tokens(test_coins: list[BaseCoin], client: AsyncClient):
# pass
#


async def test_clear_observer(
    client: AsyncClient,
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData, MongoBaseUser],
):
    db, tokens, user = get_user_data
    headers = {"Authorization": f"Bearer {tokens.access}"}
    response = await client.delete("/observer/clear", headers=headers)
    assert response.status_code == 204

    service = ObserverService(db, user)
    crud = service.crud

    await service.clear_observer()
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0

    headers = {"Authorization": f"Bearer {tokens.access}"}
    response = await client.delete("/observer/clear", headers=headers)
    assert response.status_code == 204

    await service.clear_observer()
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0
