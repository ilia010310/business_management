import uuid
from typing import Union

from src.api.v1.auth.auth_dependencies import validate_auth_user
from src.utils import jwt_utils as auth_utils
from src.schemas.account import AccountSchema
from src.schemas.token import TokenInfo
from src.tasks.tasks import send_invite_code_to_email
from fastapi import APIRouter, Depends, status
from pydantic import EmailStr
from src.api.dependencies import UOWDep
from src.schemas.sing_up import SingUpSchema, SingUpCompleteSchema
from src.schemas.user import CreateUserSchema
from src.servises.account import AccountService
from src.servises.user import UserService
from src.servises.invite import InviteService
from src.utils.generator_invite_codes import generator_invite_codes
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/auth/v1", tags=["Auth"])


@router.get("/check_account")
async def register_employee(email: EmailStr, uow: UOWDep) -> dict:
    """Генерирует проверочеый код,
    Добавляет информацию в приглашения,
    Отправляет приглашение на почту"""
    code = generator_invite_codes()
    result = await AccountService().checking_account_and_send_invitation(uow, email, code)
    if result:
        return {"exists": True, "message": "This email is already taken."}
    send_invite_code_to_email.delay(email, code)
    return {"exists": False, "message": "This email does not exist."}


@router.post("/sing-up")
async def sing_up(data: SingUpSchema, uow: UOWDep) -> dict:
    """Проверяет валидность проверочного кода"""
    result = await InviteService().checking_invitation(uow, data)
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Forbidden")
    return {"status": "success"}


@router.post("/sing-up-complete")
async def sing_up_complete(data: SingUpCompleteSchema, uow: UOWDep) -> dict:
    """Создает компанию, юзера-администратора, сохраняет пароль и почту"""
    result: uuid = await AccountService().create_company(uow, dict(data))
    if result:
        return {"status": "success"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Is not success")

@router.post("/login", response_model=TokenInfo)
async def auth_user(
    account: AccountSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": account.id,
        "email": account.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
