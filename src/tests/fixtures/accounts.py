import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security.http import HTTPAuthorizationCredentials
from accounts.crud import create_user
from auth.schemas import TokenData
from auth.services import ObtainTokenPair


@pytest.fixture
async def get_user_data(
    mongo_test_data,
) -> tuple[AsyncIOMotorDatabase, TokenData]:
    _, db = mongo_test_data
    await create_user(db, "111")
    payload = {"user_id": "111"}
    tokens = ObtainTokenPair().obtain_token_pair(payload)
    return db, tokens


@pytest.fixture
async def get_user_credentials(
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData]
) -> tuple[AsyncIOMotorDatabase, HTTPAuthorizationCredentials]:
    db, tokens = get_user_data
    credentials = HTTPAuthorizationCredentials(credentials=tokens.access, scheme="Bear")
    return db, credentials
