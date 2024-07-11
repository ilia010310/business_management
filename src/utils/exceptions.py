from fastapi import HTTPException


class UserDuplicationError(HTTPException):
    pass
