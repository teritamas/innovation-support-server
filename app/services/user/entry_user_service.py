from app.facades.database import users_store
from app.schemas.user.domain import AccountType, User
from app.schemas.user.requests import EntryStandardUserRequest
from app.utils.common import generate_id_str
from app.utils.logging import logger


def execute(request: EntryStandardUserRequest) -> str:
    users = users_store.fetch_user_from_wallet_address(request.wallet_address)

    if users != []:  # 存在する場合はそのユーザIDを返す
        logger.info(f"users is exists. {users=}")
        return users[0].user_id

    # 存在しない場合は新規に作成する。
    user_id = generate_id_str()
    user = User.parse_obj(request.dict())
    user.user_id = user_id
    user.account_type = AccountType.STANDARD
    users_store.add_user(id=user_id, content=user)

    return user_id
