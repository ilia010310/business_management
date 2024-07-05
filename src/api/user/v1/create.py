from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep

from src.api.user.v1.dependencies.jwt_dependencies import get_current_account
from src.schemas.user import *
from src.schemas.response import ResponseCreateNewUser
from src.servises.user import UserService

router = APIRouter(prefix="/user/v1", tags=["Data operations"])


@router.post("/send_invite", response_model=ResponseCreateNewUser)
async def create_new_user(
    uow: UOWDep, new_user: CreateUserSchema, account: AccountSchema = Depends(get_current_account)
):
    """Создает нового сотрудника, привязывает его к компании,
    отправляет приглашение на почту"""
    new_user: CreateUserSchemaAndEmailAndId = await UserService().add_one_user_for_company(uow, new_user, account)
    return ResponseCreateNewUser(
        status=201,
        error=False,
        payload=new_user,
        detail="The new user has been created",
    )
