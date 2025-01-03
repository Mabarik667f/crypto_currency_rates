import jwt
from core import settings
from .schemas import TokenData, TokenRefresh
from auth.exceptions import RefreshError
from datetime import datetime, timedelta, timezone
from loguru import logger


class ObtainTokenPair:

    def __init__(
        self,
        exp_ref: timedelta = timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS),
        exp_access: timedelta = timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MIN),
    ):
        self.refresh_exp = exp_ref
        self.access_exp = exp_access

    def obtain_token_pair(self, payload: dict) -> TokenData:
        access = create_jwt_token(payload, expires_delta=self.access_exp)
        refresh = create_jwt_token(
            payload | dict(type="refresh"), expires_delta=self.refresh_exp
        )
        return TokenData(access=access, refresh=refresh)


def create_jwt_token(payload: dict, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = dict(exp=expire) | payload
    token = jwt.encode(
        payload=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return token


def refresh_tokens(refresh: TokenRefresh) -> TokenData:
    payload = jwt.decode(
        refresh.refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    user_id: str | int = payload.get("user_id")
    if payload.get("type") != "refresh" or user_id is None:
        raise RefreshError("Invalid token")
    return ObtainTokenPair().obtain_token_pair(payload)
