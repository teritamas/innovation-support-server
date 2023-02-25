from typing import List

from app.facades.database import fire_store
from app.schemas.user.domain import User

COLLECTION_PREFIX = "users"


def add_user(id: str, content: User):
    """ユーザを新規追加する

    Args:
        id (str): UserId
        content (User): 追加するユーザ情報
    """
    fire_store.add(collection=COLLECTION_PREFIX, id=id, content=content.dict())


def fetch_user(id: str) -> User | None:
    """idからユーザ情報を検索する。

    Args:
        id (str): ユーザ情報

    Returns:
        User | None:
    """
    user_dict = fire_store.fetch(collection=COLLECTION_PREFIX, id=id)
    return User.parse_obj(user_dict) if user_dict else None


def fetch_user_from_wallet_address(wallet_address: str) -> List[User]:
    """WalletAddressからユーザを検索する。

    Args:
        wallet_address (str): 検索対象のWalletアドレス

    Returns:
        List[User]: 検索で見つかったユーザの一覧（Walletアドレスはユニークなので、基本的に配列サイズは 0 or 1）
    """
    users = (
        fire_store()
        .collection(COLLECTION_PREFIX)
        .where("wallet_address", "==", wallet_address)
        .stream()
    )

    return [User.parse_obj(user.to_dict()) for user in users]
