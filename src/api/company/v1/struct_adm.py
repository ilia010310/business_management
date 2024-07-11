from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep
from src.api.user.v1.dependencies.jwt_dependencies import get_current_account
from src.schemas.company.struct_adm import CreateNewStructAdmSchema, StructAdmSchema
from src.schemas.response.company.struct_adm import ResponseCreateNewStructAdm, ResponseDeleteStructAdm
from src.schemas.user import AccountSchema
from src.servises.company import CompanyService

router = APIRouter(prefix="/company/v1/struct_adm", tags=["Company operations"])


@router.post("/", response_model=ResponseCreateNewStructAdm)
async def create_struct_adm(
    uow: UOWDep, struct_adm: CreateNewStructAdmSchema, account: AccountSchema = Depends(get_current_account)
):
    new_struct_adm: StructAdmSchema = await CompanyService().add_new_struct_adm(uow, struct_adm, account)
    return ResponseCreateNewStructAdm(
        status=201,
        error=False,
        payload=new_struct_adm,
        detail="The position successfully created",
    )


@router.delete("/{struct_adm_id}", response_model=ResponseDeleteStructAdm)
async def delete_struct_adm(uow: UOWDep, struct_adm_id: int, account: AccountSchema = Depends(get_current_account)):
    await CompanyService().delete_struct_adm(uow, struct_adm_id)
    return ResponseDeleteStructAdm(
        status=204,
        error=False,
        payload={},
        detail="The struct_adm successfully deleted",
    )
