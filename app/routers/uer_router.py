from fastapi import APIRouter, Depends

from app.schemas.auth.domain import AuthorizedClientSchema
from app.schemas.user.requests import EntryUserRequest
from app.schemas.user.response import DetailUserResponse, EntryUserResponse
from app.services.user import (
    detail_user_by_wallet_address_service,
    detail_user_service,
    entry_user_service,
)
from app.utils.authorization import authenticate_key

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post(
    "", description="ユーザ登録API.", response_model=EntryUserResponse
)
def entry_user(request: EntryUserRequest):
    user_id = entry_user_service.execute(request=request)
    return EntryUserResponse(user_id=user_id)


@user_router.get(
    "/{user_id}", description="ユーザ詳細取得API.", response_model=DetailUserResponse
)
def detail_user(
    user_id: str,
    _: AuthorizedClientSchema = Depends(authenticate_key),
):
    user = detail_user_service.execute(user_id)
    return DetailUserResponse(**user.dict())


@user_router.get(
    "/wallet_address/{wallet_address}",
    description="ユーザ詳細取得API.",
    response_model=DetailUserResponse,
)
def detail_user_by_wallet_address(
    wallet_address: str,
    _: AuthorizedClientSchema = Depends(authenticate_key),
):
    user = detail_user_by_wallet_address_service.execute(wallet_address)
    return DetailUserResponse(**user.dict())
