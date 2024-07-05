from typing import Annotated, Type

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDep: Type[IUnitOfWork] = Annotated[IUnitOfWork, Depends(UnitOfWork)]


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/v1/login",
)
