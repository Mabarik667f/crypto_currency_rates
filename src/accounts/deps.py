from fastapi.exceptions import HTTPException
import jwt
from typing import Annotated
from fastapi import Depends, status
from core import settings
from core.deps import MongoDep
from auth.deps import AuthDep
from .crud import get_user_by_id
from .schemas import MongoUser
from loguru import logger


async def get_current_tg_user(db: MongoDep, token: AuthDep) -> MongoUser:
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
    return MongoUser.serializer(user)


TGUserDep = Annotated[MongoUser, Depends(get_current_tg_user)]
