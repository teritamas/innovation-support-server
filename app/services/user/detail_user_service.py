from app.schemas.user.domain import User
from app.facades.firebase import user_store


def execute(user_id) -> User | None:
    return user_store.fetch_user(id=user_id)
