from pydantic import BaseModel, Field


class EntryStandardUserRequest(BaseModel):
    user_name: str = Field("", description="ユーザ名")
    wallet_address: str = Field("", description="ユーザ名")
