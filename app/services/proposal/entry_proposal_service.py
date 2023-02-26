import base64

from fastapi import UploadFile

from app import config
from app.facades.database import proposals_store, users_store
from app.facades.notification import slack
from app.facades.storage import proposal_pdf
from app.facades.web3 import proposal_nft
from app.schemas.proposal.domain import Proposal
from app.schemas.proposal.requests import EntryProposalRequest
from app.utils.common import build_nft_uri, generate_id_str
from app.utils.logging import logger


async def execute(request: EntryProposalRequest, file: UploadFile) -> str:
    try:
        proposal_user = users_store.fetch_user(request.user_id)
        if proposal_user is None:
            logger.info(f"user is none. {request.user_id=}")
            return None

        proposal_id = generate_id_str()

        nft_uri = await _upload_file(request, file, proposal_id)

        # TODO:  ここでコントラクトの書き込み処理
        nft_token_id = await proposal_nft.mint(
            proposal_user.wallet_address, identifier=nft_uri
        )

        # FireStoreに保存するフォーマットに変換
        proposal = Proposal.parse_obj(request.dict())
        proposal.proposal_id = proposal_id
        proposal.nft_token_id = nft_token_id
        proposal.nft_uri = nft_uri
        proposal.file_original_name = file.filename

        proposals_store.add_proposal(id=proposal_id, content=proposal)

        if request.slack_notification_channels:  # チャンネルが登録されている場合のみ通知をする
            logger.info(
                f"slack channel. {request.slack_notification_channels=}"
            )
            slack.broadcast(
                incoming_webhooks_url=config.default_slack_incoming_webhooks_url,
                channels=request.slack_notification_channels,
                proposal_view_url=f"{config.frontend_url}propose/{proposal.proposal_id}",
            )
        return proposal_id

    except Exception as e:
        logger.info("error", e)


async def _upload_file(request, file, proposal_id) -> str:
    """ファイルをGoogle Cloud Storageにアップロードする"""
    data = await file.read()  # アップロードされた画像をbytesに変換する処理
    bin_data: bytes = base64.b64encode(data).decode()

    nft_uri = build_nft_uri(
        request.user_id,
        proposal_id,
        file.filename,
    )
    proposal_pdf.upload(
        data=bin_data,
        destination_blob_name=nft_uri,
    )

    return nft_uri
