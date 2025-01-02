from fastapi import APIRouter, Response, status
from loguru import logger
from src.core.deps import MongoDep
from accounts.crud import create_user

router = APIRouter(tags=["accounts"], prefix="/accounts")


@router.post("/auth/telegram")
async def auth(db: MongoDep):
    user_id = str(await db.accounts.count_documents({}) + 1)
    await create_user(db, user_id)
    return Response(status_code=status.HTTP_201_CREATED)
