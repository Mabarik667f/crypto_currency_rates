import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security.http import HTTPAuthorizationCredentials
from datetime import timedelta
from accounts.schemas import MongoBaseUser, MongoUser
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
async def get_test_user(mongo_test_data) -> tuple[AsyncIOMotorDatabase, MongoBaseUser]:
    _, db = mongo_test_data
    await create_user(db, "111")
    return db, MongoBaseUser(user_id="111")


@pytest.fixture
async def get_user_data(
    get_test_user: tuple[AsyncIOMotorDatabase, MongoBaseUser]
) -> tuple[AsyncIOMotorDatabase, TokenData, MongoBaseUser]:
    db, user = get_test_user
    payload = {"user_id": user.user_id}
    tokens = ObtainTokenPair().obtain_token_pair(payload)
    return db, tokens, user


@pytest.fixture
async def get_user_credentials(
    get_user_data: tuple[AsyncIOMotorDatabase, TokenData, MongoBaseUser]
) -> tuple[AsyncIOMotorDatabase, HTTPAuthorizationCredentials]:
    db, tokens, _ = get_user_data
    credentials = HTTPAuthorizationCredentials(credentials=tokens.access, scheme="Bear")
    return db, credentials
