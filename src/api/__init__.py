__all__ = ["router"]

from fastapi import APIRouter
from src.api.user.v1.registration import router as router_auth
from src.api.user.v1.create import router as router_create_new_user
from src.api.user.v1.change_data import router as router_change_data
from src.api.tasks.v1.create import router as router_task_create
from src.api.tasks.v1.delete import router as router_task_delete
from src.api.tasks.v1.change import router as router_task_change

router = APIRouter()
router.include_router(router_auth)
router.include_router(router_create_new_user)
router.include_router(router_change_data)
router.include_router(router_task_create)
router.include_router(router_task_delete)
router.include_router(router_task_change)
