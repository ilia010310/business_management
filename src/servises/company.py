import uuid
from typing import Sequence, Any

from fastapi import HTTPException, status
from sqlalchemy import Row
from sqlalchemy_utils import Ltree

from src.models import CompanyModel, AccountModel, MembersModel, StructAdmModel, UserModel, UserPositionModel
from src.schemas.company.company import DeleteCompanySchema
from src.schemas.company.position import CreatePositionSchema, PositionSchema
from src.schemas.company.struct_adm import CreateNewStructAdmSchema, StructAdmSchema
from src.schemas.company.user_position import UserPositionSchema
from src.schemas.user import AccountSchema
from src.utils.unitofwork import IUnitOfWork


class CompanyService:
    @staticmethod
    async def _get_company_id_from_account(uow: IUnitOfWork, account: AccountSchema):
        account: AccountModel | None = await uow.account.get_by_query_one_or_none(id=account.id)
        if not account.active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a active user")
        members: MembersModel | None = await uow.members.get_by_query_one_or_none(user=account.user_id)
        if not members.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a company admin")
        company_id: uuid.UUID = members.company
        return company_id

    async def delete_company(self, uow: IUnitOfWork, company_id: uuid.UUID) -> DeleteCompanySchema:
        async with uow:
            company: CompanyModel | None = await uow.company.get_by_query_one_or_none(
                id=company_id,
            )
            if not company:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company doesn't exist")

            await uow.position.delete_by_query(company_id=company.id)
            await uow.struct_adm.delete_by_query(company_id=company.id)
            await uow.task.delete_by_query(company_id=company_id)
            users: Sequence[UserModel] = await uow.members.get_by_query_all(company=company_id)
            users_id = [user.id for user in users]
            await uow.account.delete_accounts(users_id)
            await uow.user.delete_users(users_id)
            company_name = company.name
            await uow.company.delete_by_query(id=company_id)
            return DeleteCompanySchema(name=company_name)

    async def add_new_position(
            self,
            uow: IUnitOfWork,
            position: CreatePositionSchema,
            account: AccountSchema,
    ) -> PositionSchema:
        async with uow:
            company_id = await self._get_company_id_from_account(uow, account)
            new_position = await uow.position.add_one_and_get_obj(name=position.name, company_id=company_id)
            return new_position.to_pandentic_schema()

    async def add_new_struct_adm(
            self,
            uow: IUnitOfWork,
            new_struct_adm: CreateNewStructAdmSchema,
            account: AccountSchema,
    ) -> StructAdmSchema:
        async with uow:
            company_id = await self._get_company_id_from_account(uow, account)
            if new_struct_adm.parent == new_struct_adm.name:
                try:
                    struct_adm: StructAdmModel = await uow.struct_adm.add_one_and_get_obj(
                        name=new_struct_adm.name, company_id=company_id, path=Ltree(new_struct_adm.parent)
                    )
                    return struct_adm.to_pydantic_schema()
                except Exception:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT, detail="Incorrect parent or name already exists"
                    )
            parent_struct_adm: Ltree | None = await uow.struct_adm.get_all_path_of_parent(new_struct_adm.parent)
            if not parent_struct_adm:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parent doesn't exist")
            try:
                struct_adm: StructAdmModel = await uow.struct_adm.add_one_and_get_obj(
                    name=new_struct_adm.name,
                    company_id=company_id,
                    path=Ltree(str(parent_struct_adm) + f".{new_struct_adm.name}"),
                )
                return struct_adm.to_pydantic_schema()
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Incorrect parent or name already exists"
                )

    async def delete_position(
            self,
            uow: IUnitOfWork,
            position_id: int,
    ) -> None:
        async with uow:
            await uow.position.delete_by_query(id=position_id)

    async def delete_struct_adm(
            self,
            uow: IUnitOfWork,
            struct_adm_id: int,
    ) -> None:
        async with uow:
            children: Sequence[Row[tuple[Any, ...] | Any]] = await uow.struct_adm.get_children_paths(struct_adm_id)
            await uow.struct_adm.change_children_paths(children)
            await uow.struct_adm.delete_by_query(id=struct_adm_id)

    async def add_users_to_position(
            self,
            uow: IUnitOfWork,
            users_id: list[uuid.UUID],
            position_id: int,
    ) -> list[UserPositionSchema]:
        async with uow:
            list_users_position = []
            for user_id in users_id:
                user_position: UserPositionModel = await uow.user_position.add_one_and_get_obj(user=user_id,
                                                                                               position=position_id)
                list_users_position.append(user_position.to_pydantic_schema())
            return list_users_position

    async def add_struct_adm_to_position(
            self,
            uow: IUnitOfWork,
            struct_adm_id: int,
            position_id: int,
    ) -> StructAdmSchema:
        async with uow:
            struct_adm_position = await uow.struct_adm_position

