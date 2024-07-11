__all__ = ["router"]

from fastapi import APIRouter
from src.api.user.v1.registration import router as router_auth
from src.api.user.v1.create import router as router_create_new_user
from src.api.user.v1.change_data import router as router_change_data
from src.api.tasks.v1.tasks import router as router_task_create
from src.api.company.v1.company import router as router_delete_company
from src.api.company.v1.position import router as router_add_position
from src.api.company.v1.struct_adm import router as router_struct_adm

router = APIRouter()
router.include_router(router_auth)
router.include_router(router_create_new_user)
router.include_router(router_change_data)
router.include_router(router_task_create)
router.include_router(router_delete_company)
router.include_router(router_add_position)
router.include_router(router_struct_adm)
