from app.facades.database import (
    proposal_votes_store,
    proposals_store,
    users_store,
)
from app.facades.web3 import inosapo_ft
from app.schemas.user.domain import User
from app.schemas.user.dto import DetailUserDto


def execute(user_id) -> DetailUserDto | None:
    user = users_store.fetch_user(id=user_id)

    if user is None:
        return None

    balance: int = inosapo_ft.balance_of_address(user.wallet_address)
    updated_user: User = users_store.update_token_amount(
        user_id=user.user_id, balance=balance
    )

    dto = DetailUserDto(**updated_user.dict())

    user_own_proposals = proposals_store.fetch_proposals_by_user_id(
        user_id=user_id
    )
    dto.proposals = user_own_proposals

    user_own_votes = proposal_votes_store.fetch_proposal_vote_by_user_id(
        user_id=user_id
    )
    dto.proposal_votes = user_own_votes

    return dto
