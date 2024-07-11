import uuid

from fastapi import APIRouter, Depends

from src.api.dependencies import UOWDep
from src.api.user.v1.dependencies.jwt_dependencies import get_current_account
from src.schemas.company.company import DeleteCompanySchema
from src.schemas.response import ResponseCreateNewTask, ResponseDeleteCompany
from src.schemas.user import AccountSchema
from src.servises.company import CompanyService

router = APIRouter(prefix="/company/v1", tags=["Company operations"])


@router.delete("/{company_id}", response_model=ResponseDeleteCompany)
async def delete_company(uow: UOWDep, company_id: uuid.UUID, account: AccountSchema = Depends(get_current_account)):
    company_name: DeleteCompanySchema = await CompanyService().delete_company(uow, company_id)
    return ResponseCreateNewTask(
        status=204,
        error=False,
        payload=company_name,
        detail="The company successfully deleted",
    )
