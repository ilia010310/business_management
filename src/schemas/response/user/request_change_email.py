from src.schemas.response import ResponseBase
from src.schemas.user import RequestChangeEmailSchema


class ResponseRequestChangeEmail(ResponseBase):
    payload: RequestChangeEmailSchema
