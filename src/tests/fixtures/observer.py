from accounts.schemas import MongoUser
import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from cryptowrapper.schemas import BaseCoin
from observer.services import ObserverService
from observer.crud import ObserverCrud
from loguru import logger


@pytest.fixture(scope="function")
async def get_observer_crud(
    get_test_user: tuple[AsyncIOMotorDatabase, MongoUser]
) -> ObserverCrud:
    db, user = get_test_user
    return ObserverCrud(db, user.user_id)


@pytest.fixture(scope="function")
async def get_observer_service(
    get_test_user: tuple[AsyncIOMotorDatabase, MongoUser],
) -> ObserverService:
    db, user = get_test_user
    return ObserverService(db, user)


@pytest.fixture(scope="function")
async def set_observed_coins(
    get_observer_crud: ObserverCrud, test_coins: list[BaseCoin]
) -> None:
    crud = get_observer_crud
    coins_ids = ["bitcoin", "ethereum", "bnb"]
    await crud.add_observed_coins(coins_ids)
