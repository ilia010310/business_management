import uuid

from pydantic import BaseModel, Field, UUID4, EmailStr


class IdUserSchema(BaseModel):
    id: UUID4


class CreateUserSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    middle_name: str | None = Field(max_length=50, default=None)


class UserSchema(IdUserSchema, CreateUserSchema):
    pass


class CreateUserSchemaAndEmailAndId(CreateUserSchema):
    id: uuid.UUID
    email: EmailStr


class UpdateUserSchema(IdUserSchema):
    first_name: str | None = Field(max_length=50, default=None)
    last_name: str | None = Field(max_length=50, default=None)
    middle_name: str | None = Field(max_length=50, default=None)


class RequestChangeEmailSchema(BaseModel):
    old_email: EmailStr
    new_email: EmailStr
    user_id: uuid.UUID
