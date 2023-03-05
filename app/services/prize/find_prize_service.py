from typing import List

from app.facades.database import prizes_store
from app.schemas.prize.domain import Prize


def execute() -> List[Prize]:
    return prizes_store.find_prize()
