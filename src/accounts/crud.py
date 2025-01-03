from motor.motor_asyncio import AsyncIOMotorDatabase
from .exceptions import UserNotFoundError


async def create_user(db: AsyncIOMotorDatabase, user_id: int | str) -> None:
    await db.accounts.find_one_and_update(
        {"user_id": str(user_id)}, {"$set": {"user_id": str(user_id)}}, upsert=True
    )


async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: int | str) -> dict:
    user = await db.accounts.find_one({"user_id": str(user_id)})
    if user is None:
        raise UserNotFoundError(field="user_id", msg="User not found")
    return user
