import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from src.api.dependencies import UOWDep
from src.api.user.v1.registration import register_employee
from src.api.user.v1.dependencies.jwt_dependencies import get_current_account
from src.models.user import UserModel
from src.schemas.response import ResponseCreateNewUser, ResponseRequestChangeEmail
from src.schemas.user.account import AccountSchema
from src.schemas.user import CreateUserSchema, CreateUserSchemaAndEmailAndId, RequestChangeEmailSchema
from src.servises.account import AccountService
from src.servises.invite import InviteService
from src.servises.user import UserService

router = APIRouter(prefix="/user/v1", tags=["Data operations"])


@router.post("/ditail")
async def change_ditail(
        uow: UOWDep,
        new_data: CreateUserSchema,
        account: AccountSchema = Depends(get_current_account)

) -> ResponseCreateNewUser:
    user: CreateUserSchemaAndEmailAndId = await AccountService().change_ditail(uow, account, new_data)
    return ResponseCreateNewUser(
        status=201,
        error=False,
        payload=user,
        detail="The user successfully updated the information",
    )



@router.post("/change_email")
async def request_for_change_email(
        uow: UOWDep,
        email: EmailStr,
        account: AccountSchema = Depends(get_current_account),

) -> ResponseRequestChangeEmail:
    request_for_change: RequestChangeEmailSchema = await UserService().request_for_change_email(uow, email, account)

    return ResponseRequestChangeEmail(
        status=200,
        error=False,
        payload=request_for_change,
        detail="The new user has been created",
    )


@router.post("/confirm_email")
async def confirm_email(
        uow: UOWDep,
        code: int,
        account: AccountSchema = Depends(get_current_account)

) -> dict:
    try:
        email: EmailStr = await InviteService().get_email(uow, code)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Code unvalidated")
    await AccountService().change_email(uow, account.id, email)
    return {
        "status": "success",
        "detail": "email changed"
    }
