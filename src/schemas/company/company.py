import uuid

from pydantic import BaseModel, Field, EmailStr


class CompanySchema(BaseModel):
    name: str = Field(max_length=50)


class CreateCompanySchema(BaseModel):
    company_id: uuid.UUID
    company_name: str
    admin: uuid.UUID
    email: EmailStr
