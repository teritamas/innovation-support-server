from app.facades.database import users_store
from app.schemas.user.domain import AccountType, User
from app.schemas.user.requests import UpdateStandardUserRequest
from app.schemas.user.response import UpdateStandardUserResponse
from app.utils.logging import logger


def execute(user_id: str, request: UpdateStandardUserRequest) -> User:
    user = users_store.fetch_user(user_id)

    if user is None:  # 存在する場合はそのユーザIDを返す
        logger.warn(f"users is not exists. {request.mail_address}")
        RuntimeError

    user = user
    user.wallet_address = request.wallet_address
    user.account_type = AccountType.STANDARD

    users_store.add_user(id=user.user_id, content=user)

    return user
