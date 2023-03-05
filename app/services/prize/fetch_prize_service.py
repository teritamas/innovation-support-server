from app.facades.database import prizes_store
from app.schemas.prize.domain import Prize


def execute(prize_id: str) -> Prize | None:
    return prizes_store.fetch_prize(prize_id)
