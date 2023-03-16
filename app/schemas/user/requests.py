from pydantic import BaseModel, Field


class EntryUserRequest(BaseModel):
    user_name: str = Field("", description="ユーザ名")

    wallet_address: str = Field("", description="ウォレットアドレス")
    mail_address: str = Field("", description="メールアドレス.ウォレットアドレスが含まれている場合は不要")


class UpdateStandardUserRequest(BaseModel):
    wallet_address: str = Field(..., description="ウォレットアドレス")
