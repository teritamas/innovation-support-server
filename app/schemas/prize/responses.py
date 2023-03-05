from typing import List

from pydantic import BaseModel, Field

from app.schemas.prize.domain import Prize


class FindPrizeResponse(BaseModel):
    prizes: List[Prize] = Field([], description="登録されている景品の一覧")


class FetchPrizeResponse(Prize):
    pass


class EntryPrizeResponse(BaseModel):
    prize_id: str = Field("", description="景品ID")


class EntryPrizeTradeResponse(BaseModel):
    balance: int = Field(..., description="景品交換後の残高")
