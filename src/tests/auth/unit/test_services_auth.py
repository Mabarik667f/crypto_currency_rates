import pytest
from datetime import timedelta
from jwt.exceptions import DecodeError
from auth.services import create_jwt_token, refresh_tokens, ObtainTokenPair
from auth.exceptions import RefreshError
from auth.schemas import TokenData, TokenRefresh
from core import settings


@pytest.fixture
def payload() -> dict:
    return {"user_id": 1}

@pytest.fixture
def payload_refresh() -> dict:
    return {"user_id": 1, "type": "refresh"}

@pytest.fixture
def get_refresh(payload_refresh: dict) -> TokenRefresh:
    return TokenRefresh(refresh=create_jwt_token(
            payload_refresh, timedelta(minutes=settings.JWT_REFRESH_EXPIRE_DAYS)
        ))

def test_create_access_token(payload: dict):
    access = create_jwt_token(
        payload, timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MIN)
    )
    assert len(access) >= 120


def test_create_refresh_token(payload_refresh: dict):
    refresh = create_jwt_token(
        payload_refresh, timedelta(minutes=settings.JWT_REFRESH_EXPIRE_DAYS)
    )
    assert len(refresh) >= 140


def test_obtain_token_pair(payload: dict):
    tokens = ObtainTokenPair().obtain_token_pair(payload)
    assert isinstance(tokens, TokenData)


def test_refresh_tokens(get_refresh: TokenRefresh):
    tokens = refresh_tokens(get_refresh)
    assert isinstance(tokens, TokenData)

    with pytest.raises(DecodeError) as exc:
        refresh_tokens(TokenRefresh(refresh="dasdada"))
        assert exc.value == "Not enough segments"

    with pytest.raises(RefreshError) as exc:
        refresh = create_jwt_token(
            {}, timedelta(minutes=settings.JWT_REFRESH_EXPIRE_DAYS)
        )
        refresh_tokens(TokenRefresh(refresh=refresh))
        assert exc.value == "Invalid token"
