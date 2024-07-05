__all__ = ["router"]

from fastapi import APIRouter
from src.api.user.v1.registration import router as router_auth
from src.api.user.v1.create import router as router_create_new_user
from src.api.user.v1.change_data import router as router_change_data

router = APIRouter()
router.include_router(router_auth)
router.include_router(router_create_new_user)
router.include_router(router_change_data)
