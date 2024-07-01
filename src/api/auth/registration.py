from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep
from src.schemas.user import CreateUserSchema
from src.servises.user import UserService
from src.utils.unitofwork import IUnitOfWork

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/employee")
async def register_employee(
        employee: CreateUserSchema,
        uow: UOWDep
):
    result = await UserService().add_one(uow, employee)
    return result

