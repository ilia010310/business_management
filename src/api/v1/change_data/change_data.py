import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from src.api.dependencies import UOWDep
from src.api.v1.auth.registration import register_employee
from src.api.v1.create_new_user.create_dependencies import get_current_account
from src.schemas.account import AccountSchema
from src.schemas.user import CreateUserSchema
from src.servises.account import AccountService
from src.servises.invite import InviteService
from src.servises.user import UserService

router = APIRouter(prefix="/user/v1", tags=["Data operations"])


@router.post("/names")
async def change_names(
        uow: UOWDep,
        new_data: CreateUserSchema,
        account: AccountSchema = Depends(get_current_account)

) -> dict:
    user_id: uuid.UUID = await AccountService().get_company_id(uow, account)
    await UserService().change_names(uow, user_id, new_data)
    return {
        "status": "success",
        "detail": "usernames changed"
    }


@router.post("/change_email")
async def request_for_change_email(
        uow: UOWDep,
        email: EmailStr,
        account: AccountSchema = Depends(get_current_account),

):
    existence_check = await register_employee(email, uow)
    if existence_check.get("exists"):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This email is already taken")
    return {
        "status": "success",
        "detail": "verification code sent by email"
    }


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
