import base64

from fastapi import UploadFile
from pdf2image import convert_from_bytes

from app import config
from app.facades.database import proposals_store, timelines_store, users_store
from app.facades.notification import slack
from app.facades.storage import proposal_pdf, proposal_thumbnail_image
from app.facades.web3 import inosapo_ft, proposal_nft, proposal_vote
from app.schemas.proposal.domain import (
    Proposal,
    ProposalFundraisingCondition,
    ProposalPhase,
    ProposalStatus,
)
from app.schemas.proposal.requests import EntryProposalRequest
from app.utils.common import build_nft_uri, generate_id_str, now
from app.utils.logging import logger


async def execute(
    user_id: str, request: EntryProposalRequest, file: UploadFile
) -> str:
    try:
        logger.info(f"entry proposal . {user_id=}, {request=}")
        proposal_user = users_store.fetch_user(user_id)
        if proposal_user is None:
            # authorization.pyで認証しているため、ここがNoneになることはほぼない。
            # その為Errorログを出しておく
            logger.error(f"user is none. {user_id=}")
            return None

        proposal_id = generate_id_str()
        file_bytes_data = await file.read()  # アップロードされた画像をbytesに変換する処理

        thumbnail_filename: str = await _upload_thumbnail_image_from_pdf(
            proposal_id=proposal_id, file=file_bytes_data
        )
        nft_uri = await _upload_file(
            user_id, proposal_id, file.filename, file_bytes_data
        )

        proposal_fundraising_condition = build_condition(
            request.proposal_phase
        )

        # TODO:  ここでコントラクトの書き込み処理
        nft_token_id = await proposal_nft.mint(
            proposal_user.wallet_address,
            identifier=nft_uri,
            amount=proposal_fundraising_condition.procurement_token_amount,
        )
        await inosapo_ft.transfer_to_vote_contract(
            proposal_fundraising_condition.procurement_token_amount
        )
        await proposal_vote.entry_proposal(tokenId=nft_token_id)

        # FireStoreに保存するフォーマットに変換
        proposal = Proposal.parse_obj(request.dict())
        proposal.user_id = proposal_user.user_id
        proposal.proposal_id = proposal_id
        proposal.nft_token_id = nft_token_id
        proposal.nft_uri = nft_uri
        proposal.proposal_status = ProposalStatus.VOTING
        proposal.created_at = now()
        proposal.updated_at = now()
        proposal.file_original_name = file.filename
        proposal.thumbnail_filename = thumbnail_filename
        proposal.proposal_fundraising_condition = (
            proposal_fundraising_condition
        )

        proposals_store.add_proposal(id=proposal_id, content=proposal)
        timelines_store.add_timeline(content=proposal)

        if (
            request.slack_notification_channels
            and config.default_slack_incoming_webhooks_url == ""
        ):  # チャンネルが登録されている場合のみ通知をする
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


def build_condition(phase: ProposalPhase) -> ProposalFundraisingCondition:
    if phase == ProposalPhase.SEED:
        limit_date = 7
        procurement_token_amount = 50  # 500千円
        min_voter_count = 50
        min_agreement_count = 0.5

    elif phase == ProposalPhase.EARLY:
        limit_date = 7
        procurement_token_amount = 100  # 1,000千円
        min_voter_count = 100
        min_agreement_count = 0.5
    elif phase == ProposalPhase.MIDDLE:
        limit_date = 14
        procurement_token_amount = 500  # 5,000千円
        min_voter_count = 200
        min_agreement_count = 0.6
    elif phase == ProposalPhase.LATER:
        limit_date = 21
        procurement_token_amount = 1000  # 10,000千円
        min_voter_count = 300
        min_agreement_count = 0.7
    elif phase == ProposalPhase.GROWTH:
        limit_date = 21
        procurement_token_amount = 5000  # 50,000千円
        min_voter_count = 500
        min_agreement_count = 0.8

    return ProposalFundraisingCondition.parse_obj(
        {
            "limit_date": limit_date,
            "procurement_token_amount": procurement_token_amount,
            "min_voter_count": min_voter_count,
            "min_agreement_count": min_agreement_count,
        }
    )


async def _upload_file(
    user_id: str,
    proposal_id: str,
    filename: str,
    file: bytes,
) -> str:
    """ファイルをGoogle Cloud Storageにアップロードする"""
    bin_data: bytes = base64.b64encode(file).decode()

    nft_uri = build_nft_uri(
        user_id,
        proposal_id,
        filename,
    )
    proposal_pdf.upload(
        data=bin_data,
        destination_blob_name=nft_uri,
    )

    return nft_uri


async def _upload_thumbnail_image_from_pdf(
    proposal_id: str, file: bytes
) -> str:
    """pdfからサムネイル画像を生成しGoogle Cloud Storageに保存する"""
    thumbnail_filename = f"{proposal_id}.jpeg"
    images = convert_from_bytes(
        file,
    )
    proposal_thumbnail_image.upload(
        destination_blob_name=thumbnail_filename, image=images[0]
    )
    return thumbnail_filename
