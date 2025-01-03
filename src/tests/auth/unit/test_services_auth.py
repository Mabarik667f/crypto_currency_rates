import pytest
from datetime import timedelta
from auth.services import create_jwt_token, ObtainTokenPair
from auth.schemas import TokenData
from core import settings


@pytest.fixture
def payload() -> dict:
    return {"user_id": 1}


async def test_create_access_token(payload: dict):
    access = create_jwt_token(
        payload, timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MIN)
    )
    assert len(access) >= 120


async def test_create_refresh_token(payload: dict):
    payload = payload | dict(type="refresh")
    access = create_jwt_token(
        payload, timedelta(minutes=settings.JWT_REFRESH_EXPIRE_DAYS)
    )
    assert len(access) >= 140


async def test_obtain_token_pair(payload: dict):
    tokens = ObtainTokenPair().obtain_token_pair(payload)
    assert isinstance(tokens, TokenData)
