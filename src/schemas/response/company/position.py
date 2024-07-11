from src.schemas.company.position import PositionSchema
from src.schemas.response import ResponseBase


class ResponseCreateNewPosition(ResponseBase):
    payload: PositionSchema


class ResponseDeletePosition(ResponseBase):
    payload: dict
