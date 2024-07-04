from pydantic import BaseModel, Field, conint


class SingUpSchema(BaseModel):
    account: str = Field(max_length=50)
    invite_token: conint(ge=1000, le=9999)


class SingUpCompleteSchema(BaseModel):
    account: str = Field(max_length=50)
    password: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    company_name: str = Field(max_length=50)
