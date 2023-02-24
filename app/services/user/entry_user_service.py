from app.facades.firebase import user_store
from app.schemas.user.domain import User
from app.schemas.user.requests import EntryUserRequest
from app.utils.common import generate_id_str


def execute(request: EntryUserRequest) -> str:
    users = user_store.fetch_user_from_wallet_address(request.wallet_address)

    if users != []:  # 存在する場合はそのユーザIDを返す
        return users[0].user_id

    # 存在しない場合は新規に作成する。
    user_id = generate_id_str()
    user = User.parse_obj(request.dict())
    user.user_id = user_id
    user_store.add_user(id=user_id, content=user)

    return user_id
