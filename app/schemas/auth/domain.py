from pydantic import BaseModel, Field


class AuthorizedClientSchema(BaseModel):
    user_id: str = Field("", description="UserId")
