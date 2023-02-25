from app.schemas.user.domain import User
from app.facades.firebase import users_store


def execute(user_id) -> User | None:
    return users_store.fetch_user(id=user_id)
