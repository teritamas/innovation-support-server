from app.facades.database import prizes_store
from app.schemas.prize.domain import Prize
from app.schemas.prize.requests import EntryPrizeRequest
from app.utils.common import generate_id_str, now


def execute(user_id: str, request: EntryPrizeRequest) -> str:
    prize_id = generate_id_str()

    prize = Prize.parse_obj(request.dict())
    prize.prize_id = prize_id
    prize.user_id = user_id
    prize.created_at = now()
    prize.updated_at = now()
    prizes_store.add_prize(prize_id, prize)

    return prize_id
