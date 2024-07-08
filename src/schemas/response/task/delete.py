from src.schemas.response import ResponseBase
from src.schemas.task.task import DeleteTaskSchema


class ResponseDeleteTask(ResponseBase):
    payload: DeleteTaskSchema
