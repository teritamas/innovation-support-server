from fastapi import APIRouter, Depends

from app.schemas.auth.domain import AuthorizedClientSchema
from app.schemas.prize.requests import EntryPrizeRequest
from app.schemas.prize.responses import (
    EntryPrizeResponse,
    EntryPrizeTradeResponse,
    FindPrizeResponse,
)
from app.services.prize import entry_prize_service
from app.utils.authorization import authenticate_key

prize_router = APIRouter(prefix="/prize", tags=["prize"])


@prize_router.get(
    "",
    description="トークンと交換可能なコンテンツの一覧を表示する",
    response_model=FindPrizeResponse,
)
def find_prize():
    return FindPrizeResponse()


@prize_router.post(
    "",
    description="トークンと交換可能なコンテンツを追加する",
    response_model=EntryPrizeResponse,
)
def entry_prize(
    request: EntryPrizeRequest,
    auth: AuthorizedClientSchema = Depends(authenticate_key),
):
    prize_id = entry_prize_service.execute(auth.user_id, request)
    return EntryPrizeResponse(prize_id=prize_id)


@prize_router.post(
    "{prize_id}/trade",
    description="指定した景品をトークンと交換する。",
    response_model=EntryPrizeTradeResponse,
)
def entry_prize_trade(
    prize_id: str,
    auth: AuthorizedClientSchema = Depends(authenticate_key),
):
    return EntryPrizeTradeResponse()
