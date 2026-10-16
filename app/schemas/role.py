from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    name: str

class RoleSchema(RoleBase):
    """Role data returned by the API."""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)