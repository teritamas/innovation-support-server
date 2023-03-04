from app.facades.database import (
    proposal_votes_store,
    proposals_store,
    users_store,
)
from app.schemas.user.dto import DetailUserDto


def execute(user_id) -> DetailUserDto | None:
    user = users_store.fetch_user(id=user_id)

    if user is None:
        return None

    dto = DetailUserDto(**user.dict())

    user_own_proposals = proposals_store.fetch_proposals_by_user_id(
        user_id=user_id
    )
    dto.proposals = user_own_proposals

    user_own_votes = proposal_votes_store.fetch_proposal_vote_by_user_id(
        user_id=user_id
    )
    dto.proposal_votes = user_own_votes

    return dto
