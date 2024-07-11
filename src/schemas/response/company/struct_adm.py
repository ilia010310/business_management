from src.schemas.company.struct_adm import StructAdmSchema
from src.schemas.response import ResponseBase


class ResponseCreateNewStructAdm(ResponseBase):
    payload: StructAdmSchema


class ResponseDeleteStructAdm(ResponseBase):
    payload: dict
