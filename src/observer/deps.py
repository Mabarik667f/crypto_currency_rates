from typing import Annotated
from auth.deps import TGUserDep
from core.deps import MongoDep
from fastapi import Depends
from observer.services import ObserverService


async def get_observer_service(db: MongoDep, user: TGUserDep) -> ObserverService:
    return ObserverService(db, user)


ObserverServDep = Annotated[ObserverService, Depends(get_observer_service)]
