from fastapi import APIRouter, status
from observer.deps import ObserverServDep
from loguru import logger

router = APIRouter(tags=["observer"], prefix="/observer")


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def observe_clear(service: ObserverServDep):
    await service.clear_observer()
