import uuid

from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep
from src.api.user.v1.dependencies.jwt_dependencies import get_current_account
from src.schemas.company.position import PositionSchema, CreatePositionSchema
from src.schemas.company.struct_adm import StructAdmSchema
from src.schemas.company.user_position import UserPositionSchema
from src.schemas.response import ResponseCreateNewTask, ResponseAddUsersToPosition
from src.schemas.response.company.position import ResponseCreateNewPosition, ResponseDeletePosition
from src.schemas.response.company.struct_adm_position import ResponseAddStructAdmToPosition
from src.schemas.user import AccountSchema
from src.servises.company import CompanyService

router = APIRouter(prefix="/company/v1/position", tags=["Company operations"])


@router.post("/", response_model=ResponseCreateNewPosition)
async def create_position(
        uow: UOWDep, new_position: CreatePositionSchema, account: AccountSchema = Depends(get_current_account)
):
    position: PositionSchema = await CompanyService().add_new_position(uow, new_position, account)
    return ResponseCreateNewTask(
        status=201,
        error=False,
        payload=position,
        detail="The position successfully created",
    )


@router.delete("/{position_id}", response_model=ResponseDeletePosition)
async def delete_position(uow: UOWDep, position_id: int, account: AccountSchema = Depends(get_current_account)):
    await CompanyService().delete_position(uow, position_id)
    return ResponseDeletePosition(
        status=204,
        error=False,
        payload={},
        detail="The position successfully deleted",
    )


@router.post("/{position_id}/add_users", response_model=ResponseAddUsersToPosition)
async def add_users_to_position(uow: UOWDep, position_id: int,
                                users: list[uuid.UUID],
                                account: AccountSchema = Depends(get_current_account)):
    users_position: list[UserPositionSchema] = await CompanyService().add_users_to_position(uow, users, position_id)
    return ResponseAddUsersToPosition(
        status=201,
        error=False,
        payload=users_position,
        detail="The users successfully added to position",
    )


@router.post("/{position_id}/add_struct_adm", response_model=ResponseAddStructAdmToPosition)
async def add_struct_adm_to_position(uow: UOWDep, position_id: int,
                                     struct_adm_id: int,
                                     account: AccountSchema = Depends(get_current_account)):
    struct_adm_position: StructAdmSchema = await CompanyService().add_struct_adm_to_position(uow, struct_adm_id,
                                                                                             position_id)
    return ResponseAddStructAdmToPosition(
        status=201,
        error=False,
        payload=struct_adm_position,
        detail="The users successfully added to position",
    )
