from fastapi import APIRouter
from api.v1.endpoints import cr_router, observer_router, auth_router

v1_router = APIRouter()

v1_router.include_router(cr_router)
v1_router.include_router(observer_router)
v1_router.include_router(auth_router)
