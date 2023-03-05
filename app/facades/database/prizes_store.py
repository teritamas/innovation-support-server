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


def fetch_prize(
    id,
) -> Prize | None:
    """景品を取得する"""

    prize_dict = fire_store.fetch(collection=COLLECTION_PREFIX, id=id)
    return Prize.parse_obj(prize_dict) if prize_dict else None


def find_prize() -> List[Prize]:
    """景品を全て取得する"""

    prizes = fire_store().collection(COLLECTION_PREFIX).stream()
    return [Prize.parse_obj(prize.to_dict()) for prize in prizes]


def fetch_prize(id: str) -> Prize | None:
    """idから景品情報を検索する。

    Args:
        id (str): 景品情報

    Returns:
        Prize | None:
    """
    prize_dict = fire_store.fetch(collection=COLLECTION_PREFIX, id=id)
    return Prize.parse_obj(prize_dict) if prize_dict else None


def find_prize() -> List[Prize]:
    """景品を全て取得する"""

    prizes = fire_store().collection(COLLECTION_PREFIX).stream()
    return [Prize.parse_obj(prize.to_dict()) for prize in prizes]


def fetch_prize(id: str) -> Prize | None:
    """idから景品情報を検索する。

    Args:
        id (str): 景品情報

    Returns:
        Prize | None:
    """
    prize_dict = fire_store.fetch(collection=COLLECTION_PREFIX, id=id)
    return Prize.parse_obj(prize_dict) if prize_dict else None
