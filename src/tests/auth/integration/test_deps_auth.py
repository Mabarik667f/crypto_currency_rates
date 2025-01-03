import pytest
from accounts.schemas import MongoUser
from jwt.exceptions import DecodeError
from fastapi.security.http import HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase
from auth.deps import get_current_tg_user


async def test_get_current_tg_user(
    get_user_credentials: tuple[AsyncIOMotorDatabase, HTTPAuthorizationCredentials]
):
    db, credentials = get_user_credentials
    user = await get_current_tg_user(db, credentials)
    assert isinstance(user, MongoUser)

    with pytest.raises(DecodeError) as exc:
        credentials.credentials = "dadada"
        await get_current_tg_user(db, credentials)
        assert exc.value == "Not enough segments"
