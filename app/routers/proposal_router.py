import os

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks

from app.facades.database.proposals_store import fetch_proposal
from app.schemas.auth.domain import AuthorizedClientSchema
from app.schemas.proposal.requests import EntryProposalRequest
from app.schemas.proposal.responses import (
    DetailProposalResponse,
    EntryProposalResponse,
    FetchVoteStatusResponse,
    FindProposalResponse,
)
from app.services.proposal import (
    download_proposal_attachment_service,
    download_proposal_thumbnail_service,
    entry_proposal_service,
    fetch_proposal_service,
    fetch_proposal_vote_status_service,
    find_proposal_service,
)
from app.utils.authorization import authenticate_key


def remove_file(path: str) -> None:
    os.unlink(path)


proposal_router = APIRouter(prefix="/proposal", tags=["proposal"])


@proposal_router.post(
    "", description="提案登録API.", response_model=EntryProposalResponse
)
async def entry_proposal(
    background_tasks: BackgroundTasks,
    request: EntryProposalRequest = Body(...),
    file: UploadFile = File(...),
    auth: AuthorizedClientSchema = Depends(authenticate_key),
):
    proposal_id = await entry_proposal_service.execute(
        background_tasks=background_tasks,
        user_id=auth.user_id,
        request=request,
        file=file,
    )
    return EntryProposalResponse(proposal_id=proposal_id)


@proposal_router.get(
    "/{proposal_id}",
    description="提案詳細取得API.",
    response_model=DetailProposalResponse,
)
def detail_proposal(
    proposal_id: str,
):
    proposal, user = fetch_proposal_service.execute(proposal_id=proposal_id)
    if proposal and user:
        proposal.user_id = user.user_id
        return DetailProposalResponse(
            proposal=proposal,
            proposal_user=user,
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@proposal_router.get(
    "/{proposal_id}/attachment",
    description="提案詳細PDF取得API.",
    response_class=FileResponse,
    response_description="提案に紐づくPDFファイル",
)
def download_proposal_attachment(
    proposal_id: str,
    background_tasks: BackgroundTasks,
    _: AuthorizedClientSchema = Depends(authenticate_key),
):
    response = download_proposal_attachment_service.execute(
        proposal_id=proposal_id
    )
    if response:
        background_tasks.add_task(remove_file, response)  # 実行後ファイルを削除
        return FileResponse(
            path=response,
            media_type="application/pdf",
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@proposal_router.get(
    "/{proposal_id}/thumbnail",
    description="サムネイル取得API.",
    response_class=FileResponse,
    response_description="提案のサムネイル",
)
def download_proposal_thumbnail(
    proposal_id: str,
    background_tasks: BackgroundTasks,
):
    response = download_proposal_thumbnail_service.execute(
        proposal_id=proposal_id
    )
    if response:
        background_tasks.add_task(remove_file, response)  # 実行後ファイルを削除
        return FileResponse(
            path=response,
            media_type="image/jpeg",
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@proposal_router.get(
    "/{proposal_id}/vote_status",
    description="提案に対する投票状態取得API.",
    response_model=FetchVoteStatusResponse,
)
def fetch_proposal_vote_status(
    proposal_id: str,
    auth: AuthorizedClientSchema = Depends(authenticate_key),
):
    """提案の投票状態を取得する。ユーザが投票済みでない場合は何も返さない"""
    dto = fetch_proposal_vote_status_service.execute(
        auth.user_id, proposal_id=proposal_id
    )

    if dto:
        response = FetchVoteStatusResponse.parse_obj(dto.dict())
        response.vote_action = False
        return response
    else:
        return FetchVoteStatusResponse(
            vote_action=True,
            positive_proposal_votes=[],
            negative_proposal_votes=[],
        )


@proposal_router.get(
    "",
    description="提案一覧取得API.",
    response_model=FindProposalResponse,
)
def find_proposal(
    user_id: str | None = None,
    status: str | None = None,
    title: str | None = None,
    description: str | None = None,
    tag: str | None = None,
):
    # TODO: タグで絞り込みは未実施
    proposals = find_proposal_service.execute(
        user_id=user_id,
        proposal_status=status,
        title=title,
        description=description,
        tag=tag,
    )
    return FindProposalResponse(proposals=proposals)
