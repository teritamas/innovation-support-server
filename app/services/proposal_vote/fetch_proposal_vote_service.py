from app.facades.database.proposal_votes_store import (
    fetch_proposal_vote_by_proposal_id_and_user_id,
)
from app.schemas.proposal_vote.domain import ProposalVote


def execute(proposal_id: str, vote_user_id: str) -> ProposalVote | None:
    proposal_vote = fetch_proposal_vote_by_proposal_id_and_user_id(
        proposal_id, vote_user_id
    )

    return proposal_vote[0] if proposal_vote != [] else None
