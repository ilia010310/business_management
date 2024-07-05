from pydantic import BaseModel


class ResponseBase(BaseModel):
    status: int
    error: bool
    detail: str
