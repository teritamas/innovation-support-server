from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.prize.domain import Prize, PrizeLevel
from app.utils.common import now


class UserPurchasedPrize(BaseModel):
    prize_id: str = Field("", description="交換可能な景品のId")
    name: str = Field(..., max_length=256, description="景品名")
    description: str = Field(..., max_length=8192, description="景品の概要")
    required_token_amount: PositiveInt = Field(1, description="景品の交換に必要なトークン")
    recommendation_score: float = Field(3, description="おすすめ度")
    level: PrizeLevel = Field(PrizeLevel.MIDDLE, description="難易度")

    user_id: str = Field("", description="作成したユーザID")
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
    total_exchangeable_token: float = Field(
        0, description="保有トークンのうち現金に交換可能なトークン量"
    )

    purchased_prizes: List[UserPurchasedPrize] = Field(
        [], description="このユーザが購入した研修"
    )
