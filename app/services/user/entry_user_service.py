from app.facades.database import users_store
from app.schemas.user.domain import AccountType, User
from app.schemas.user.requests import EntryUserRequest
from app.utils.common import generate_id_str
from app.utils.logging import logger


def execute(request: EntryUserRequest) -> str:
    users = users_store.fetch_user_from_wallet_address(request.wallet_address)

    if users == [0]:  # 存在する場合はそのユーザIDを返す
        logger.info(f"users is exists. {users=}")
        return users[0].user_id

    # 存在しない場合は新規に作成する。
    user_id = generate_id_str()
    user = User.parse_obj(request.dict())
    user.user_id = user_id

    if _is_standard_account_register(
        request.wallet_address, request.mail_address
    ):
        user.account_type = AccountType.STANDARD
    elif _is_temp_account_register(
        request.wallet_address, request.mail_address
    ):
        user.account_type = AccountType.TEMP
    else:
        logger.error(f"WalletAddressとMailAddressの両方が空です。処理を終了します")
        RuntimeError

    users_store.add_user(id=user_id, content=user)

    return user_id


def _is_standard_account_register(wallet_address: str, mail_address: str):
    """Standardアカウントで登録する場合True"""
    return (wallet_address != "" and mail_address == "") or (
        wallet_address != "" and mail_address != ""
    )


def _is_temp_account_register(wallet_address: str, mail_address: str):
    """Tempアカウントで登録する場合True"""
    return wallet_address == "" and mail_address != ""
