from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.account import AccountSchema
from src.servises.account import AccountService
from src.utils import jwt_utils as auth_utils
from src.api.dependencies import UOWDep, oauth2_scheme
from jwt.exceptions import InvalidTokenError


async def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
) -> dict:
    print(token)
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
            # detail=f"invalid token error",
        )
    return payload


async def get_current_auth_account(
        uow: UOWDep,
        payload: dict = Depends(get_current_token_payload),
) -> AccountSchema:
    account_id: str = payload.get("sub")
    account: AccountSchema = await AccountService().get_one_account(uow, account_id)
    if account:
        return account
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def get_current_account(
        account: AccountSchema = Depends(get_current_auth_account),
):
    if account.active:
        return account
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="account inactive",
    )
