from fastapi import APIRouter, HTTPException, status

from app.schemas.user.requests import (
    EntryUserRequest,
    UpdateStandardUserRequest,
)
from app.schemas.user.response import (
    DetailUserResponse,
    EntryUserResponse,
    UpdateStandardUserResponse,
)
from app.services.user import (
    detail_user_by_mail_address_service,
    detail_user_by_wallet_address_service,
    entry_user_service,
    signup_standard_service,
)

account_router = APIRouter(prefix="", tags=["account"])


@account_router.post(
    "/signup", description="サインアップ.", response_model=EntryUserResponse
)
def signup(request: EntryUserRequest):
    dto = entry_user_service.execute(request=request)
    return EntryUserResponse(**dto.dict())


@account_router.get(
    "/login/wallet_address/{wallet_address}",
    description="ウォレットアドレスからユーザ情報を取得.",
    response_model=DetailUserResponse,
)
def login_wallet_address(
    wallet_address: str,
):
    user = detail_user_by_wallet_address_service.execute(wallet_address)
    if user:
        return DetailUserResponse(**user.dict())
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@account_router.get(
    "/login/mail_address/{mail_address}",
    description="メールアドレスからユーザ情報を取得.",
    response_model=DetailUserResponse,
)
def login_mail_address(
    mail_address: str,
):
    user = detail_user_by_mail_address_service.execute(mail_address)
    if user:
        return DetailUserResponse(**user.dict())
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@account_router.patch(
    "/signup/{user_id}/standard",
    description="TempユーザをStandardユーザに更新する.",
    response_model=UpdateStandardUserResponse,
)
def signup_standard(
    user_id: str,
    request: UpdateStandardUserRequest,
):
    user = signup_standard_service.execute(user_id, request)
    if user:
        return UpdateStandardUserResponse(**user.dict())
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
