from pydantic import BaseModel, Field


class CompanySchema(BaseModel):
    name: str = Field(max_length=50)
