from motor.motor_asyncio import AsyncIOMotorDatabase


async def create_user(db: AsyncIOMotorDatabase, user_id: int | str) -> None:
    await db.accounts.find_one_and_update(
        {"user_id": str(user_id)}, {"$set": {"user_id": str(user_id)}}, upsert=True
    )
