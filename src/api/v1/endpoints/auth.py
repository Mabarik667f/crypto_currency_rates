from auth.schemas import TokenData, TokenRefresh
from fastapi import APIRouter, status
from loguru import logger
from core.deps import MongoDep
from accounts.crud import create_user
from auth.services import ObtainTokenPair, refresh_tokens
from auth.deps import TGCheckDep, TGUserDep

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/telegram")
async def relegram_auth(db: MongoDep, tg: TGCheckDep) -> TokenData:
    await create_user(db, tg.user_id)
    payload = {"user_id": tg.user_id}
    tokens = ObtainTokenPair().obtain_token_pair(payload)
    return tokens


@router.post("/refresh", status_code=status.HTTP_201_CREATED)
async def refresh(user: TGUserDep, refresh: TokenRefresh) -> TokenData:
    return refresh_tokens(refresh)
