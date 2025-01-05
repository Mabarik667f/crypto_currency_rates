import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security.http import HTTPAuthorizationCredentials
from datetime import timedelta
from accounts.schemas import MongoUser
from accounts.crud import create_user, get_user_by_id
from auth.schemas import TokenRefresh, TokenData
from auth.services import create_jwt_token, ObtainTokenPair
from core import settings


@pytest.fixture
def get_refresh(payload_refresh: dict) -> TokenRefresh:
    return TokenRefresh(
        refresh=create_jwt_token(
            payload_refresh, timedelta(minutes=settings.JWT_REFRESH_EXPIRE_DAYS)
        )
    )


@pytest.fixture
async def get_test_user(mongo_test_data) -> tuple[AsyncIOMotorDatabase, MongoUser]:
    _, db = mongo_test_data
    await create_user(db, "111")
    return db, MongoUser.serializer(await get_user_by_id(db, "111"))


@pytest.fixture
async def get_user_data(
    get_test_user: tuple[AsyncIOMotorDatabase, MongoUser]
) -> tuple[AsyncIOMotorDatabase, TokenData]:
    db, user = get_test_user
    payload = {"user_id": user.user_id}
    tokens = ObtainTokenPair().obtain_token_pair(payload)
    return db, tokens


@pytest.fixture
async def get_user_credentials(
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData]
) -> tuple[AsyncIOMotorDatabase, HTTPAuthorizationCredentials]:
    db, tokens = get_user_data
    credentials = HTTPAuthorizationCredentials(credentials=tokens.access, scheme="Bear")
    return db, credentials
