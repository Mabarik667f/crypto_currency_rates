import pytest
from datetime import timedelta
from auth.schemas import TokenRefresh
from auth.services import create_jwt_token
from core import settings


@pytest.fixture
def get_refresh(payload_refresh: dict) -> TokenRefresh:
    return TokenRefresh(
        refresh=create_jwt_token(
            payload_refresh, timedelta(minutes=settings.JWT_REFRESH_EXPIRE_DAYS)
        )
    )
