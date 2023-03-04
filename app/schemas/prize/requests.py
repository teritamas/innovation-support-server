from pydantic import BaseModel, Field, PositiveInt

from app.schemas.prize.domain import PrizeLevel


class EntryPrizeRequest(BaseModel):
    name: str = Field(..., max_length=256, description="景品名")
    description: str = Field(..., max_length=8192, description="景品の概要")
    required_token_amount: PositiveInt = Field(1, description="景品の交換に必要なトークン")
    recommendation_score: float = Field(3, description="おすすめ度")
    level: PrizeLevel = Field(PrizeLevel.MIDDLE, description="難易度")
