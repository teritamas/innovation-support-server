from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.schemas.prize.domain import Prize
from app.utils.common import now


class UserPurchasedPrize(Prize):
    purchased_date: datetime = Field(now(), description="購入時刻")


class User(BaseModel):
    """ユーザドメイン"""

    user_id: str = Field("", description="ユーザID")
    user_name: str = Field("", description="ユーザ名")
    message: str = Field("", description="一言メッセージ")

    created_at: datetime = Field(now(), description="作成時刻")
    updated_at: datetime = Field(now(), description="編集時刻")

    wallet_address: str = Field("", description="ユーザに紐づくウォレットのアドレス")
    total_token_amount: float = Field(0, description="ユーザの保持トークンの総量")

    purchased_prizes: List[UserPurchasedPrize] = Field(
        [], description="このユーザが購入した研修"
    )
