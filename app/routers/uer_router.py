from fastapi import APIRouter
from app.schemas.user.requests import EntryUserRequest

from app.schemas.user.response import DetailUserResponse, EntryUserResponse


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("", description="ユーザ登録API.", response_model=EntryUserResponse)
def entry_user(request: EntryUserRequest):
    return EntryUserResponse()


@user_router.get(
    "/{user_id}", description="提案詳細取得API.", response_model=DetailUserResponse
)
def detail_user(user_id: str):
    return DetailUserResponse()
