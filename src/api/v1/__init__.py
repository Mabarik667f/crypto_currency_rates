from fastapi import APIRouter
from api.v1.endpoints import cr_router, accounts_router

v1_router = APIRouter()

v1_router.include_router(cr_router)
v1_router.include_router(accounts_router)
