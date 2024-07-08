from src.schemas.response import ResponseBase
from src.schemas.task import TaskSchema


class ResponseCreateNewTask(ResponseBase):
    payload: TaskSchema
