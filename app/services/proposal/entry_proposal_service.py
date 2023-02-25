import base64
import os
from typing import List

from fastapi import UploadFile

from app.facades.firebase import proposals_store
from app.facades.gcs import proposal_pdf
from app.facades.web3 import proposal_nft
from app.schemas.proposal.domain import Proposal
from app.schemas.proposal.requests import EntryProposalRequest
from app.utils.common import generate_id_str


async def execute(request: EntryProposalRequest, file: UploadFile) -> str:
    try:
        data = await file.read()  # アップロードされた画像をbytesに変換する処理
        bin_data: bytes = base64.b64encode(data).decode()

        proposal_id = generate_id_str()
        bucket_path = os.path.join(
            request.proposer_wallet_address, proposal_id, file.filename
        )
        proposal_pdf.upload(
            data=bin_data,
            destination_blob_name=bucket_path,
        )

        # TODO:  ここでコントラクトの書き込み処理
        nft_token_id = proposal_nft.mint(
            request.proposer_wallet_address, identifier=bucket_path
        )

        # FireStoreに保存するフォーマットに変換
        proposal = Proposal.parse_obj(request.dict())
        proposal.proposal_id = proposal_id
        proposal.nft_token_id = nft_token_id
        proposal.bucket_path = bucket_path

        proposals_store.add_proposal(id=proposal_id, content=proposal)
        return proposal_id

    except Exception as e:
        print("error", e)
