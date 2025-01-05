import jwt
from typing import Annotated
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.exceptions import HTTPException
from auth.exceptions import TelegramAuthError
from core import settings
from core.deps import MongoDep
from accounts.crud import get_user_by_id
from accounts.schemas import MongoBaseUser, MongoUser
from loguru import logger

from .schemas import TelegramHash


security = HTTPBearer()
AuthDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]


# mock realisation
def check_auth(hash: TelegramHash) -> TelegramHash:
    if hash.hash != "1111":
        raise TelegramAuthError(field="hash", msg="Auth error")
    return hash


TGCheckDep = Annotated[TelegramHash, Depends(check_auth)]


async def get_current_tg_user(db: MongoDep, token: AuthDep) -> MongoBaseUser:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(
        token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    user_id: str | int = payload.get("user_id")
    if user_id is None:
        raise credentials_exc

    user = await get_user_by_id(db, user_id)
    return MongoBaseUser(user_id=user["user_id"])


TGUserDep = Annotated[MongoUser, Depends(get_current_tg_user)]
