import base64
import os

from fastapi.responses import FileResponse

from app.facades.firebase import proposals_store
from app.facades.gcs import proposal_pdf
from app.schemas.proposal.domain import Proposal


def execute(proposal_id: str, bucket_path: str) -> str:
    # TODO: bucket_pathで正しいかを確認
    proposal: Proposal = proposals_store.fetch_proposal(proposal_id)
    if proposal is None:  # IDに紐づく提案が存在しなければNoneを返す
        print("proposal is None")
        return None

    download_byte = proposal_pdf.download(proposal.bucket_path)
    with open(os.path.basename(proposal.bucket_path), "wb") as f:
        f.write(base64.b64decode(download_byte))

    return os.path.basename(proposal.bucket_path)
