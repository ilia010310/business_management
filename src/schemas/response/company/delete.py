from src.schemas.company.company import DeleteCompanySchema
from src.schemas.response import ResponseBase


class ResponseDeleteCompany(ResponseBase):
    payload: DeleteCompanySchema
