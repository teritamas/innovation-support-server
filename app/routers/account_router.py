from fastapi import APIRouter, HTTPException, status

from app.schemas.user.requests import EntryUserRequest
from app.schemas.user.response import DetailUserResponse, EntryUserResponse
from app.services.user import (
    detail_user_by_wallet_address_service,
    entry_user_service,
)
from app.utils.authorization import authenticate_key

account_router = APIRouter(prefix="", tags=["account"])


@account_router.post(
    "/signup", description="サインアップ.", response_model=EntryUserResponse
)
def signup(request: EntryUserRequest):
    user_id = entry_user_service.execute(request=request)
    return EntryUserResponse(user_id=user_id)


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
