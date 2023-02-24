from fastapi import APIRouter
from app.schemas.proposal.requests import EntryProposalRequest
from app.schemas.proposal.responses import (
    EntryProposalResponse,
    DetailProposalResponse,
    FindProposalResponse,
)


proposal_router = APIRouter(prefix="/proposal", tags=["proposal"])


@proposal_router.post("", description="提案登録API.", response_model=EntryProposalResponse)
def entry_proposal(request: EntryProposalRequest):
    return EntryProposalResponse()


@proposal_router.get(
    "/{proposal_id}", description="提案詳細取得API.", response_model=DetailProposalResponse
)
def detail_proposal(proposal_id: str):
    return DetailProposalResponse()


@proposal_router.get("", description="提案一覧取得API.", response_model=FindProposalResponse)
def find_proposal(tags: str | None = None, words: str | None = None):
    return FindProposalResponse()
