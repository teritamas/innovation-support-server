from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

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
    background_tasks: BackgroundTasks,
    proposal_id: str,
    request: EntryProposalVoteRequest,
    auth: AuthorizedClientSchema = Depends(authenticate_key),
):
    """提案に対して投票を行う"""
    dto = entry_proposal_vote_service.execute(
        background_tasks=background_tasks,
        user_id=auth.user_id,
        proposal_id=proposal_id,
        request=request,
    )
    if dto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return EntryProposalVoteResponse(
        reward=dto.reword,
        balance=dto.balance,
    )


@proposal_vote_router.get(
    "/{proposal_id}/vote",
    response_model=FetchProposalVoteResponse,
)
def fetch_proposal_vote(
    proposal_id: str,
    auth: AuthorizedClientSchema = Depends(authenticate_key),
):
    """提案に対して投票を行ったかどうかを確認する。投票済みの場合は投票した内容が返る。対象の提案の提案者が自身の場合はその旨が返る。"""
    dto: FetchProposalVoteDto = fetch_proposal_vote_service.execute(
        auth.user_id, proposal_id
    )
    return FetchProposalVoteResponse.parse_obj(dto.dict())
