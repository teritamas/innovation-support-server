from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.auth.domain import AuthorizedClientSchema
from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.proposal_vote.dto import FetchProposalVoteDto
from app.schemas.proposal_vote.requests import EntryProposalVoteRequest
from app.schemas.proposal_vote.responses import (
    EntryProposalVoteResponse,
    FetchProposalVoteResponse,
)
from app.services.proposal_vote import (
    entry_proposal_vote_service,
    fetch_proposal_vote_service,
)
from app.utils.authorization import authenticate_key

proposal_vote_router = APIRouter(prefix="/proposal", tags=["vote"])


@proposal_vote_router.post(
    "/{proposal_id}/vote",
    response_model=EntryProposalVoteResponse,
)
def entry_proposal_vote(
    proposal_id: str,
    request: EntryProposalVoteRequest,
    auth: AuthorizedClientSchema = Depends(authenticate_key),
):
    vote_nft_token_id = entry_proposal_vote_service.execute(
        auth.user_id, proposal_id, request
    )
    if vote_nft_token_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return EntryProposalVoteResponse(
        vote_nft_token_id=vote_nft_token_id, reward=10.0
    )


@proposal_vote_router.get(
    "/{proposal_id}/vote",
    response_model=FetchProposalVoteResponse,
)
def fetch_proposal_vote(
    proposal_id: str,
    auth: AuthorizedClientSchema = Depends(authenticate_key),
):
    dto: FetchProposalVoteDto = fetch_proposal_vote_service.execute(
        auth.user_id, proposal_id
    )
    return FetchProposalVoteResponse.parse_obj(dto.dict())
