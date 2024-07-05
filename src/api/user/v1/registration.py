import uuid

from src.api.user.v1.dependencies.auth_dependencies import validate_auth_user
from src.models.user import InviteModel
from src.schemas.company import CreateCompanySchema
from src.schemas.response import *
from src.schemas.user import *
from src.utils import jwt_utils as auth_utils

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from src.api.dependencies import UOWDep

from src.servises.account import AccountService
from src.servises.invite import InviteService

router = APIRouter(prefix="/auth/v1", tags=["Auth"])


@router.get("/check_account", response_model=ResponseInvite)
async def register_employee(email: EmailStr, uow: UOWDep):
    """Проверяет наличие почты в базе,
    если она не обнаружена:
     генерирует проверочеый код,
    добавляет информацию в приглашения,
    отправляет приглашение на почту"""

    invite: InviteModel = await AccountService().checking_account_and_send_invitation(uow, email)

    return {
        "status": 201,
        "error": False,
        "payload": InviteSchema(
            id=invite.id,
            email=invite.email,
            code=invite.code,
            created_at=invite.created_at,
        ),
        "detail": "invitation sent",
    }


@router.post("/sing-up", response_model=ResponseInvite)
async def sing_up(data: SingUpSchema, uow: UOWDep):
    """Проверяет валидность проверочного кода"""
    invite: InviteModel = await InviteService().checking_invitation(uow, data)
    return {
        "status": 200,
        "error": False,
        "payload": InviteSchema(
            id=invite.id,
            email=invite.email,
            code=invite.code,
            created_at=invite.created_at,
        ),
        "detail": "code is valid",
    }


@router.post("/sing-up-complete", response_model=ResponseCreateCompany)
async def sing_up_complete(data: SingUpCompleteSchema, uow: UOWDep):
    """Создает компанию, юзера-администратора, сохраняет пароль и почту"""
    company_with_user: CreateCompanySchema = await AccountService().create_company(uow, data)
    return ResponseCreateCompany(
        status=200,
        erroe=False,
        payload=company_with_user,
        detail="company created",
    )


@router.post("/login", response_model=TokenInfo)
async def auth_user(
        account: AccountSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": account.id,
        "username": account.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.post("/complete_sing_up/{user_id}/{email}", response_model=ResponseCreateNewUser)
async def complete_sing_up(
        email: EmailStr,
        user_id: uuid.UUID,
        uow: UOWDep,
        password: str,
):
    add_user_password: CreateUserSchemaAndEmailAndId = await AccountService().add_user_password(
        uow,
        user_id,
        email,
        password,
    )
    return ResponseCreateNewUser(
        status=201,
        error=False,
        payload=add_user_password,
        detail="The new user completed authorization",
    )
