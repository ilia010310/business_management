import uuid

from pydantic import BaseModel, Field, EmailStr


class CompanySchema(BaseModel):
    id: uuid.UUID
    name: str = Field(max_length=50)
    users: list
    positions: list


class CreateCompanySchema(BaseModel):
    company_id: uuid.UUID
    company_name: str
    admin: uuid.UUID
    email: EmailStr
