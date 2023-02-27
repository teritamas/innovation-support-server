from fastapi import APIRouter, HTTPException, status

from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.proposal_vote.requests import EntryProposalVoteRequest
from app.schemas.proposal_vote.responses import (
    EntryProposalVoteResponse,
    FetchProposalVoteResponse,
)
from app.services.proposal_vote import (
    entry_proposal_vote_service,
    fetch_proposal_vote_service,
)

proposal_vote_router = APIRouter(prefix="/proposal", tags=["vote"])


@proposal_vote_router.post(
    "/{proposal_id}/vote",
    response_model=EntryProposalVoteResponse,
)
def entry_proposal_vote(proposal_id: str, request: EntryProposalVoteRequest):
    vote_nft_token_id = entry_proposal_vote_service.execute(
        proposal_id, request
    )
    if vote_nft_token_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return EntryProposalVoteResponse(
        vote_nft_token_id=vote_nft_token_id, reward=10.0
    )


@proposal_vote_router.get(
    "/{proposal_id}/vote/{vote_user_id}",
    response_model=FetchProposalVoteResponse,
)
def fetch_proposal_vote(proposal_id: str, vote_user_id: str):
    response: ProposalVote | None = fetch_proposal_vote_service.execute(
        proposal_id, vote_user_id
    )
    if response is None:
        return FetchProposalVoteResponse(voted=False, vote_content=None)
    return FetchProposalVoteResponse(voted=True, vote_content=response)
