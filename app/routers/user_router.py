from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.auth.domain import AuthorizedClientSchema
from app.schemas.user.response import DetailUserResponse
from app.services.user import detail_user_service
from app.utils.authorization import authenticate_key

user_router = APIRouter(prefix="", tags=["user"])


@user_router.get(
    "/user/{user_id}",
    description="ユーザ詳細取得API.",
    response_model=DetailUserResponse,
)
def detail_user(
    user_id: str,
    _: AuthorizedClientSchema = Depends(authenticate_key),
):
    user = detail_user_service.execute(user_id)
    if user:
        return DetailUserResponse(**user.dict())
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
