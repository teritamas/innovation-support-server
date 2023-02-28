from app.facades.database import proposals_store
from app.facades.database.proposal_votes_store import (
    fetch_proposal_vote_by_proposal_id_and_user_id,
)
from app.schemas.proposal.domain import Proposal
from app.schemas.proposal_vote.dto import FetchProposalVoteDto


def execute(vote_user_id: str, proposal_id: str) -> FetchProposalVoteDto:
    proposal: Proposal = proposals_store.fetch_proposal(proposal_id)
    if proposal.user_id == vote_user_id:
        return FetchProposalVoteDto(is_proposer=True)
    proposal_vote = fetch_proposal_vote_by_proposal_id_and_user_id(
        proposal_id, vote_user_id
    )

    if proposal_vote != []:
        return FetchProposalVoteDto(
            is_proposer=False, voted=True, vote_content=proposal_vote[0]
        )
    else:
        return FetchProposalVoteDto(is_proposer=False, voted=False)
