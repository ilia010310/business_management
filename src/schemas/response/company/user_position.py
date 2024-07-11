
from src.schemas.company.user_position import UserPositionSchema
from src.schemas.response import ResponseBase


class ResponseAddUsersToPosition(ResponseBase):
    payload: list[UserPositionSchema]


