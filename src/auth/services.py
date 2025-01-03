import jwt
from .schemas import TokenData
from core import settings
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
