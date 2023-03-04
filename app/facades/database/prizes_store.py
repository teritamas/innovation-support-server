from typing import List

from app.facades.database import fire_store
from app.schemas.prize.domain import Prize

COLLECTION_PREFIX = "prizes"


def add_prize(id: str, content: Prize):
    """景品内容を新規追加する

    Args:
        id (str): prizeId
        content (prize): 追加する景品情報
    """
    fire_store.add(collection=COLLECTION_PREFIX, id=id, content=content.dict())


def find_prize() -> List[Prize]:
    """景品を全て取得する"""

    prizes = fire_store().collection(COLLECTION_PREFIX).stream()
    return [Prize.parse_obj(prize.to_dict()) for prize in prizes]
