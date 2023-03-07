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


def fetch_prize(id: str) -> Prize | None:
    """idから景品情報を検索する。

    Args:
        id (str): 景品情報

    Returns:
        Prize | None:
    """
    prize_dict = fire_store.fetch(collection=COLLECTION_PREFIX, id=id)
    return Prize.parse_obj(prize_dict) if prize_dict else None


def purchased_prize(prize_id: str, user_id: str) -> Prize | None:
    """購入したユーザのIDを追加する。

    Args:
        prize_id (str): 景品ID
        user_id (str): ユーザID

    Returns:
        Prize | None:
    """
    prize = fetch_prize(prize_id)
    if prize is None:
        return None

    prize.purchased_users.append(user_id)
    add_prize(prize_id, prize)

    return prize
