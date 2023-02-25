from app.facades.firebase import users_store
from app.schemas.user.domain import User


def execute(user_id) -> User | None:
    user = users_store.fetch_user(id=user_id)

    # TODO: ここでネットワークからウォレットの情報を取得する。
    # wallet_address = user.wallet_address
    return user
