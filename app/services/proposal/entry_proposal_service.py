import base64

from fastapi import UploadFile
from pdf2image import convert_from_bytes
from PIL import Image

from app import config
from app.facades.database import proposals_store, timelines_store, users_store
from app.facades.notification import slack
from app.facades.storage import proposal_pdf, proposal_thumbnail_image
from app.facades.web3 import proposal_nft
from app.schemas.proposal.domain import Proposal, ProposalStatus
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

        # TODO:  ここでコントラクトの書き込み処理
        nft_token_id = await proposal_nft.mint(
            proposal_user.wallet_address, identifier=nft_uri
        )

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
    thumbnail_filename = f"{proposal_id}.png"
    images = convert_from_bytes(
        file,
    )
    bin_data: bytes = base64.b64encode(image_to_byte_array(images[0])).decode()

    proposal_thumbnail_image.upload(bin_data, thumbnail_filename)
    return thumbnail_filename


import io

from PIL import Image


def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
