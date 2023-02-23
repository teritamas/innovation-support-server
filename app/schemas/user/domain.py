from pydantic import BaseModel, Field


class User(BaseModel):
    """ユーザドメイン"""

    user_id: str = Field("", description="ユーザID")
    user_name: str = Field("", description="ユーザ名")
    message: str = Field("", description="一言メッセージ")

    wallet_address: str = Field("", description="ユーザ名")
    total_token_amount: float = Field(0, description="ユーザの保持トークンの総量")
