from auth.schemas import TelegramHash, TokenData
from fastapi import APIRouter, Response, status
from loguru import logger
from core.deps import MongoDep
from accounts.crud import create_user
from auth.services import ObtainTokenPair
from auth.deps import TGCheckDep

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/telegram")
async def auth(db: MongoDep, tg: TGCheckDep) -> TokenData:
    await create_user(db, tg.user_id)
    payload = {"user_id": tg.user_id}
    tokens = ObtainTokenPair().obtain_token_pair(payload)
    return tokens
