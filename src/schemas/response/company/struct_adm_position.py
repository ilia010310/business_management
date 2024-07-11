from src.schemas.company.struct_adm_position import StructAdmPositionSchema
from src.schemas.response import ResponseBase


class ResponseAddStructAdmToPosition(ResponseBase):
    payload: StructAdmPositionSchema
