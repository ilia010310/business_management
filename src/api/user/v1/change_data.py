from fastapi import APIRouter, Depends
from pydantic import EmailStr
from src.api.dependencies import UOWDep
from src.api.user.v1.dependencies.jwt_dependencies import get_current_account
from src.schemas.response import ResponseCreateNewUser, ResponseRequestChangeEmail
from src.schemas.user.account import AccountSchema
from src.schemas.user import CreateUserSchema, CreateUserSchemaAndEmailAndId, RequestChangeEmailSchema
from src.servises.account import AccountService
from src.servises.invite import InviteService
from src.servises.user import UserService

router = APIRouter(prefix="/user/v1", tags=["Data operations"])


@router.post("/ditail", response_model=ResponseCreateNewUser)
async def change_ditail(uow: UOWDep, new_data: CreateUserSchema, account: AccountSchema = Depends(get_current_account)):
    user: CreateUserSchemaAndEmailAndId = await AccountService().change_ditail(uow, account, new_data)
    return ResponseCreateNewUser(
        status=201,
        error=False,
        payload=user,
        detail="The user successfully updated the information",
    )


@router.post("/change_email", response_model=ResponseRequestChangeEmail)
async def request_for_change_email(
    uow: UOWDep,
    email: EmailStr,
    account: AccountSchema = Depends(get_current_account),
):
    request_for_change: RequestChangeEmailSchema = await UserService().request_for_change_email(uow, email, account)

    return ResponseRequestChangeEmail(
        status=200,
        error=False,
        payload=request_for_change,
        detail="The new user has been created",
    )


@router.post("/confirm_email", response_model=ResponseRequestChangeEmail)
async def confirm_email(uow: UOWDep, code: int, account: AccountSchema = Depends(get_current_account)):
    payload: RequestChangeEmailSchema = await InviteService().check_and_change_email(uow, code, account)
    return ResponseRequestChangeEmail(
        status=201,
        error=False,
        payload=payload,
        detail="The email has been updated",
    )
