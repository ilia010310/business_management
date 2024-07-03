from fastapi import Form, HTTPException, status
from src.utils import jwt_utils as auth_utils
from src.api.dependencies import UOWDep
from src.servises.account import AccountService


async def validate_auth_user(
    uow: UOWDep,
    email: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    result = await AccountService().checking_account(uow, email)
    if not result:
        raise unauthed_exc
    account = result[0]
    if not auth_utils.validate_password(
        password=password,
        hashed_password=account.password,
    ):
        raise unauthed_exc

    return account