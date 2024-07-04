from src.schemas.response import ResponseBase
from src.schemas.user import InviteSchema


class ResponseInvite(ResponseBase):
    payload: InviteSchema

