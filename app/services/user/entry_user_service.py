from app.facades.database import users_store
from app.schemas.user.domain import AccountType, User
from app.schemas.user.dto import EntryUserService
from app.schemas.user.requests import EntryUserRequest
from app.utils.common import generate_id_str
from app.utils.logging import logger


def execute(request: EntryUserRequest) -> EntryUserService:
    users = _fetch_user(request)

    if users == [0]:  # 存在する場合はそのユーザIDを返す
        logger.info(f"users is exists. {users=}")
        return EntryUserService(
            user_id=users[0].user_id, account_type=users[0].account_type
        )

    # 存在しない場合は新規に作成する。
    user_id = generate_id_str()
    user = User.parse_obj(request.dict())
    user.user_id = user_id

    if _is_standard_account_register(
        request.wallet_address, request.mail_address
    ):
        account_type = AccountType.STANDARD
    elif _is_temp_account_register(
        request.wallet_address, request.mail_address
    ):
        account_type = AccountType.TEMP
    else:
        logger.error(f"WalletAddressとMailAddressの両方が空です。処理を終了します")
        RuntimeError

    user.account_type = account_type
    users_store.add_user(id=user_id, content=user)

    return EntryUserService(user_id=user_id, account_type=account_type)


def _fetch_user(request):
    """ユーザが存在するか検索する"""
    if request.wallet_address != "":
        users = users_store.fetch_user_from_wallet_address(
            request.wallet_address
        )
    elif request.mail_address != "":
        users = users_store.fetch_user_from_mail_address(request.mail_address)
    else:
        logger.error(f"WalletAddressとMailAddressの両方が空です。処理を終了します")
        RuntimeError
    return users


def _is_standard_account_register(wallet_address: str, mail_address: str):
    """Standardアカウントで登録する場合True"""
    return (wallet_address != "" and mail_address == "") or (
        wallet_address != "" and mail_address != ""
    )


def _is_temp_account_register(wallet_address: str, mail_address: str):
    """Tempアカウントで登録する場合True"""
    return wallet_address == "" and mail_address != ""
