__all__ = ["router"]

from fastapi import APIRouter
from src.api.v1.auth.registration import router as router_auth
from src.api.v1.create_new_user.create import router as router_create_new_user
from src.api.v1.change_data.change_data import router as router_change_data

router = APIRouter()
router.include_router(router_auth)
router.include_router(router_create_new_user)
router.include_router(router_change_data)
