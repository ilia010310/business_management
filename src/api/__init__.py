__all__ = [
    'router'
]

from fastapi import APIRouter
from src.api.auth.registration import router as router_auth

router = APIRouter()
router.include_router(router_auth)


