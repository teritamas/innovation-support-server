from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

from app.facades.database import users_store
from app.schemas.auth.domain import AuthorizedClientSchema
from app.schemas.user.domain import User
from app.utils.logging import logger

_api_key_header = APIKeyHeader(name="Authorization")


def authenticate_key(
    api_key: str = Depends(_api_key_header),
) -> AuthorizedClientSchema | None:
    if api_key is None:
        logger.warn(f"認証キーが含まれていません.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # FIXME: 暫定対応でuser_id = api_keyとする
    user: User = users_store.fetch_user(api_key)

    if user is None:
        logger.warn(f"認証失敗(PoC中なのでエラーは返さない). api_key(user_id)={api_key}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    else:
        return AuthorizedClientSchema(user_id=user.user_id)
