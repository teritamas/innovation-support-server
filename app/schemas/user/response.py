from pydantic import BaseModel, Field

from app.schemas.user.domain import User


class EntryUserResponse(BaseModel):
    user_id: str = Field("", description="ユーザID")


class DetailUserResponse(User):
    pass
