import uuid

from fastapi import APIRouter, Depends, status
from pydantic import EmailStr
from fastapi.exceptions import HTTPException

from src.api.dependencies import UOWDep
from src.api.v1.auth.registration import register_employee
from src.api.v1.create_new_user.create_dependencies import get_current_account
from src.schemas.account import AccountSchema
from src.schemas.members import CreateMembersSchema
from src.schemas.user import CreateUserSchemaAndEmail, CreateUserSchema
from src.servises.account import AccountService
from src.servises.members import MembersService
from src.servises.user import UserService

router = APIRouter(prefix="/create/v1", tags=["Data operations"])


@router.post("/send_invite")
async def create_new_user(
        uow: UOWDep,
        new_user: CreateUserSchemaAndEmail,
        account: AccountSchema = Depends(get_current_account)) -> dict:
    """Создает нового сотрудника, привязывает его к компании,
    отправляет приглашение на почту"""
    existence_check = await register_employee(new_user.email, uow)
    if existence_check.get("exists"):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This email is already taken")

    new_user_id: uuid.UUID = await UserService().add_one(uow, CreateUserSchema(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        middle_name=new_user.middle_name,
    ))

    user_id: uuid.UUID = await AccountService().get_company_id(uow, account)
    company_id: uuid.UUID = await MembersService().get_company_id_from_members(uow, user_id)
    await MembersService().add_one(
        uow,
        CreateMembersSchema(
            user=new_user_id,
            company=company_id,
        ))
    return {
        "status": "success",
        "detail": "created a new user"
    }

