from datetime import datetime

from pydantic import BaseModel, Field

from app.utils.common import now


class User(BaseModel):
    """ユーザドメイン"""

    user_id: str = Field("", description="ユーザID")
    user_name: str = Field("", description="ユーザ名")
    message: str = Field("", description="一言メッセージ")

    created_at: datetime = Field(now(), description="作成時刻")
    updated_at: datetime = Field(now(), description="編集時刻")

    wallet_address: str = Field("", description="ユーザに紐づくウォレットのアドレス")
    total_token_amount: float = Field(0, description="ユーザの保持トークンの総量")
