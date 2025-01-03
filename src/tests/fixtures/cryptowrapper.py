from httpx import AsyncClient
import pytest
import json
from cryptowrapper.schemas import BaseCoin
from cryptowrapper.crud import get_all_coins, insert_coins
from loguru import logger


@pytest.fixture
async def test_coins(
    mongo_test_data, change_dir_to_tests: None, client: AsyncClient
) -> list[BaseCoin]:
    _, db = mongo_test_data
    test_data = []
    try:
        with open("coins.json", "r") as f:
            objs = json.load(f)
        test_data = [
            BaseCoin(id=obj["id"], symbol=obj["symbol"], name=obj["name"])
            for obj in objs
        ]
        await insert_coins(db, [c.model_dump() for c in test_data])
    except FileNotFoundError:
        logger.info("File coins.json not found, call API!")
        response = await client.post("/cryptowrapper/coins")
        assert response.status_code == 201, "Api not available, test error"
        test_data = await get_all_coins(db)
    finally:
        return test_data
