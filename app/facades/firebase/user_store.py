from typing import List


from app.schemas.user.domain import User
from app.facades.firebase import fire_store

COLLECTION_PREFIX = "users"


def add_user(id: str, content: User):
    """ユーザを新規追加する

    Args:
        id (str): UserId
        content (User): 追加するユーザ情報
    """
    doc_ref = fire_store().collection(COLLECTION_PREFIX).document(id)
    doc_ref.set(content.dict())


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


def fetch_user(id: str) -> User | None:
    """idからユーザ情報を検索する。

    Args:
        id (str): ユーザ情報

    Returns:
        User | None:
    """
    user = fire_store().collection(COLLECTION_PREFIX).document(id).get()
    return User.parse_obj(user.to_dict())
