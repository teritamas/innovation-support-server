from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, PositiveInt

from app.utils.common import now


class PrizeLevel(str, Enum):
    HIGHT = "High"  # 上級者向け
    MIDDLE = "Middle"  # 中級者向け
    LOW = "Low"  # 初級者向け


class PrizeType(str, Enum):
    TRAINING = "Training"  # 研修
    WELFARE = "Welfare"  # 福利厚生


class Prize(BaseModel):
    prize_id: str = Field("", description="交換可能な景品のId")
    name: str = Field(..., max_length=256, description="景品名")
    description: str = Field(..., max_length=8192, description="景品の概要")
    required_token_amount: PositiveInt = Field(1, description="景品の交換に必要なトークン")
    recommendation_score: float = Field(3, description="おすすめ度")
    level: PrizeLevel = Field(PrizeLevel.MIDDLE, description="難易度")
    type: PrizeType = Field(PrizeType.TRAINING, description="景品の種類")

    user_id: str = Field("", description="作成したユーザID")

    purchased_users: List[str] = Field([], description="この研修を購入したユーザIDの一覧")

    created_at: datetime = Field(now(), description="作成時刻")
    updated_at: datetime = Field(now(), description="編集時刻")
