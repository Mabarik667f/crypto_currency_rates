from accounts.schemas import MongoBaseUser
from auth.schemas import TokenData
from cryptowrapper.schemas import DescribedCoin
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from observer.crud import ObserverCrud
from observer.services import ObserverService
from loguru import logger


async def test_clear_observer(
    client: AsyncClient,
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData, MongoBaseUser],
):
    db, tokens, user = get_user_data
    headers = {"Authorization": f"Bearer {tokens.access}"}
    response = await client.delete("/observer/coins/clear", headers=headers)
    assert response.status_code == 204

    service = ObserverService(db, user)
    crud = service.crud

    await service.clear_observer()
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0

    headers = {"Authorization": f"Bearer {tokens.access}"}
    response = await client.delete("/observer/coins/clear", headers=headers)
    assert response.status_code == 204

    await service.clear_observer()
    cnt = await crud.get_count_observed_coins()
    assert cnt == 0


async def test_get_observed_coins(
    client: AsyncClient,
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData, MongoBaseUser],
    set_observed_coins,
):
    _, tokens, _ = get_user_data
    headers = {"Authorization": f"Bearer {tokens.access}"}
    response = await client.get("/observer/coins", headers=headers)
    assert len(response.json()) == 3


async def test_del_observed_coins(
    client: AsyncClient,
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData, MongoBaseUser],
    set_observed_coins,
):
    _, tokens, _ = get_user_data
    headers = {"Authorization": f"Bearer {tokens.access}"}
    del_coins = {"coins_ids": ["dsadasd", "dsda"]}
    response = await client.put(
        "/observer/coins/delete",
        json=del_coins,
        headers=headers,
    )
    assert len(response.json()) == 3

    del_coins = {"coins_ids": ["dsadasd", "litecoin", "dsda", "bitcoin"]}
    response = await client.put(
        "/observer/coins/delete",
        json=del_coins,
        headers=headers,
    )
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == "ethereum"


async def test_add_observed_coins(
    client: AsyncClient,
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData, MongoBaseUser],
    set_observed_coins,
):
    _, tokens, _ = get_user_data
    headers = {"Authorization": f"Bearer {tokens.access}"}

    add_coins = {"coins_ids": ["dsadasd", "litecoin", "dsda", "bitcoin"]}
    response = await client.put(
        "/observer/coins/add",
        json=add_coins,
        headers=headers,
    )
    assert len(response.json()) == 3

    add_coins = {"coins_ids": ["dsadasd", "litecoin", "dsda", "bitcoin", "21x", "20ex"]}
    response = await client.put(
        "/observer/coins/add",
        json=add_coins,
        headers=headers,
    )
    assert len(response.json()) == 5


async def test_describe_observed_coins(
    client: AsyncClient,
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData, MongoBaseUser],
    set_observed_coins,
):
    _, tokens, _ = get_user_data
    headers = {"Authorization": f"Bearer {tokens.access}"}

    response = await client.get("/observer/coins/describe", headers=headers)
    assert len(response.json()) == 3
    assert (
        response.json()[0]["id"] != None and response.json()[0]["current_price"] != None
    )
