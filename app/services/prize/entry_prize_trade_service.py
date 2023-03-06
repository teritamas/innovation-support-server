from app.facades.database import prizes_store, users_store
from app.utils.logging import logger


def execute(user_id: str, prize_id: str) -> str | None:
    # プライズの情報を取得する
    prize = prizes_store.fetch_prize(prize_id)
    if prize is None:
        return None

    # ユーザの所有トークンを取得する
    user = users_store.fetch_user(user_id)
    user_own_token = user.total_token_amount

    # プライズの必要トークン数がユーザの所持トークンを下回っている場合、ユーザの所持トークンを減らして、プライズを購入する
    if prize.required_token_amount > user_own_token:
        logger.error(
            f"購入金額が足りません. {prize.required_token_amount=}, {user_own_token=}"
        )
        return None

    balance = users_store.reduce_token_amount(
        user_id=user_id, amount=prize.required_token_amount
    )

    updated_user = users_store.add_purchased_prize(
        user_id=user_id, prize=prize
    )
    logger.info(f"研修の追加が完了しました. {updated_user=}")

    return balance
