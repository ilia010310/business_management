

from pydantic import BaseModel


class StructAdmPositionSchema(BaseModel):
    struct_adm_id: int
    position_id: int
