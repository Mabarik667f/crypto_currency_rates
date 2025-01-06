from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError
from .exceptions import UserNotFoundError


async def create_user(db: AsyncIOMotorDatabase, user_id: int | str) -> None:
    try:
        await db.accounts.insert_one(
            {"user_id": str(user_id), "observedCoins": []},
        )
    except DuplicateKeyError:
        ...


async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: int | str) -> dict:
    user = await db.accounts.find_one({"user_id": str(user_id)})
    if user is None:
        raise UserNotFoundError(field="user_id", msg="User not found")
    return user
