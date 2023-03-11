from app.facades.database import prizes_store, users_store
from app.facades.web3 import inosapo_ft
from app.schemas.prize.domain import Prize
from app.utils.logging import logger


async def execute(user_id: str, prize_id: str) -> str | None:
    # プライズの情報を取得する
    prize = prizes_store.fetch_prize(prize_id)
    if prize is None:
        return None

    # ユーザの所有トークンを取得する
    user = users_store.fetch_user(user_id)
    # ブロックチェーン上で購入処理
    user_balance: int = inosapo_ft.balance_of_address(user.wallet_address)

    # プライズの必要トークン数がユーザの所持トークンを下回っている場合、ユーザの所持トークンを減らして、プライズを購入する
    if prize.required_token_amount > user_balance:
        logger.error(
            f"購入金額が足りません. {prize.required_token_amount=}, {user_balance=}"
        )
        users_store.update_token_amount(user_id=user_id, balance=user_balance)
        return None
    await inosapo_ft.burn(user.wallet_address, prize.required_token_amount)

    # DBの更新
    balance = update_database(user, prize_id, prize)

    return balance


def update_database(user, prize_id, prize):
    """購入内容でデータベースを更新"""
    balance = users_store.update_token_amount(
        user_id=user.user_id,
        balance=inosapo_ft.balance_of_address(user.wallet_address),
    )
    updated_user = users_store.add_purchased_prize(
        user_id=user.user_id, prize=prize
    )
    updated_prize = prizes_store.purchased_prize(
        prize_id=prize_id, user_id=user.user_id
    )

    logger.info(f"研修の追加が完了しました. {updated_user=}, {updated_prize=}")
    return balance.total_token_amount
