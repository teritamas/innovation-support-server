from fastapi import APIRouter
from app.schemas.proposal_vote.requests import EntryProposalVoteRequest

from app.schemas.proposal_vote.responses import EntryProposalVoteResponse


proposal_vote_router = APIRouter(prefix="/proposal", tags=["vote"])


@proposal_vote_router.post(
    "/{proposal_id}/vote", response_model=EntryProposalVoteResponse
)
def entry_proposal_vote(request: EntryProposalVoteRequest):
    return EntryProposalVoteResponse()
