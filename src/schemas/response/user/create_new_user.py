from src.schemas.response import ResponseBase
from src.schemas.user import CreateUserSchemaAndEmailAndId


class ResponseCreateNewUser(ResponseBase):
    payload: CreateUserSchemaAndEmailAndId
