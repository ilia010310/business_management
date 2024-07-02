import uuid
from typing import Union
from src.tasks.tasks import send_invite_code_to_email
from fastapi import APIRouter, Depends
from pydantic import EmailStr
from src.api.dependencies import UOWDep
from src.schemas.sing_up import SingUpSchema, SingUpCompleteSchema
from src.schemas.user import CreateUserSchema
from src.servises.account import AccountService
from src.servises.user import UserService
from src.servises.invite import InviteService
from src.utils.generator_invite_codes import generator_invite_codes
from src.utils.unitofwork import IUnitOfWork
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/auth/v1", tags=["Auth"])


@router.get("/check_account")
async def register_employee(email: EmailStr, uow: UOWDep) -> dict:
    code = generator_invite_codes()
    result = await AccountService().checking_account_and_send_invitation(uow, email, code)
    if result:
        return {"exists": True, "message": "This email is already taken."}
    send_invite_code_to_email.delay(email, code)
    return {"exists": False, "message": "This email does not exist."}


@router.post("/sing-up")
async def sing_up(data: SingUpSchema, uow: UOWDep) -> dict:
    result = await InviteService().checking_invitation(uow, data)
    if not result:
        raise HTTPException(status_code=403, detail="Access Forbidden")
    return {"status": "success"}


@router.post("/sing-up-complete")
async def sing_up_complete(data: SingUpCompleteSchema, uow: UOWDep) -> dict:
    result: uuid = await AccountService().create_company(uow, dict(data))
    if result:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Is not success")
