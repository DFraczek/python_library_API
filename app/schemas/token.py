from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Schema for the authentication token response."""

    access_token: str
    token_type: str = "bearer"