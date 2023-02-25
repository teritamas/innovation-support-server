import os

from fastapi import APIRouter, Body, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from app.facades.firebase.proposals_store import fetch_proposal
from app.schemas.proposal.requests import EntryProposalRequest
from app.schemas.proposal.responses import (
    DetailProposalResponse,
    EntryProposalResponse,
    FindProposalResponse,
)
from app.services.proposal import (
    download_proposal_attachment_service,
    entry_proposal_service,
    fetch_proposal_service,
    find_proposal_service,
)


def remove_file(path: str) -> None:
    os.unlink(path)


proposal_router = APIRouter(prefix="/proposal", tags=["proposal"])


@proposal_router.post(
    "", description="提案登録API.", response_model=EntryProposalResponse
)
async def entry_proposal(
    request: EntryProposalRequest = Body(...), file: UploadFile = File(...)
):
    proposal_id = await entry_proposal_service.execute(request, file)
    return EntryProposalResponse(proposal_id=proposal_id)


@proposal_router.get(
    "/{proposal_id}",
    description="提案詳細取得API.",
    response_model=DetailProposalResponse,
)
def detail_proposal(proposal_id: str):
    proposal, user = fetch_proposal_service.execute(proposal_id=proposal_id)
    if proposal and user:
        return DetailProposalResponse(
            proposal=proposal,
            proposal_user=user,
        )
    else:
        return HTTPException(status_code=404, detail="Not Found")


@proposal_router.get(
    "/{proposal_id}/attachment/{bucket_path}",
    description="提案詳細PDF取得API.",
    response_class=FileResponse,
    response_description="提案に紐づくPDFファイル",
)
def download_proposal_attachment(
    proposal_id: str, bucket_path: str, background_tasks: BackgroundTasks
):
    response = download_proposal_attachment_service.execute(
        proposal_id=proposal_id, bucket_path=bucket_path
    )
    if response:
        background_tasks.add_task(remove_file, response)  # 実行後ファイルを削除
        return FileResponse(
            path=response,
            media_type="application/pdf",
        )
    else:
        return HTTPException(status_code=404, detail="Not Found")


@proposal_router.get(
    "", description="提案一覧取得API.", response_model=FindProposalResponse
)
def find_proposal(tags: str | None = None, words: str | None = None):
    # TODO: タグで絞り込みは未実施
    proposals = find_proposal_service.execute(tags, words)
    return FindProposalResponse(proposals=proposals)
