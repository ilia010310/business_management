from src.schemas.company import CreateCompanySchema
from src.schemas.response import ResponseBase


class ResponseCreateCompany(ResponseBase):
    payload: CreateCompanySchema
