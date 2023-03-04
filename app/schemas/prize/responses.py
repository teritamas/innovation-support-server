from pydantic import BaseModel, Field

from app.schemas.prize.domain import Prize


class FindPrizeResponse(Prize):
    pass


class EntryPrizeResponse(BaseModel):
    prize_id: str = Field("", description="景品ID")


class EntryPrizeTradeResponse(BaseModel):
    prize_trade_id: str = Field("", description="景品交換ID")
