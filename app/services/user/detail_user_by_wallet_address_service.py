from app.facades.database import users_store
from app.schemas.user.domain import User


def execute(wallet_address: str) -> User | None:
    users = users_store.fetch_user_from_wallet_address(wallet_address)

    # TODO: ここでネットワークからウォレットの情報を取得する。
    # wallet_address = user.wallet_address

    return users[0] if len(users) == 1 else None
