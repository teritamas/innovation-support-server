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


def add_token_amount(user_id: str, amount: int) -> int:
    """トークンを追加する

    Args:
        user_id (str): 対象のユーザID
        amount (int): 増やすトークンの量

    Raises:
        RuntimeError: 存在しないユーザIDが指定された場合

    Returns:
        int: 計算後の残高
    """

    user = fetch_user(user_id)
    if user is None:
        raise RuntimeError(f"{user_id=} is not found.")

    balance = user.total_token_amount + amount
    user.total_token_amount = balance

    add_user(id=user_id, content=user)

    return balance


def reduce_token_amount(user_id: str, amount: int) -> int:
    """トークンを消費する

    Args:
        user_id (str): 対象のユーザID
        amount (int): 減らすトークンの量

    Raises:
        RuntimeError: 存在しないユーザIDが指定された場合

    Returns:
        int: 計算後の残高
    """

    user = fetch_user(user_id)
    if user is None:
        raise RuntimeError(f"{user_id=} is not found.")

    balance = user.total_token_amount - amount
    user.total_token_amount = balance

    add_user(id=user_id, content=user)

    return balance


def delete_user(id: str):
    fire_store.delete(collection=COLLECTION_PREFIX, id=id)
