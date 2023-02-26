import base64
import os

from fastapi.responses import FileResponse

from app.facades.database import proposals_store
from app.facades.storage import proposal_pdf
from app.schemas.proposal.domain import Proposal


def execute(proposal_id: str) -> str:
    proposal: Proposal = proposals_store.fetch_proposal(proposal_id)
    if proposal is None:  # IDに紐づく提案が存在しなければNoneを返す
        print("proposal is None")
        return None

    download_byte = proposal_pdf.download(proposal.nft_uri)
    with open(os.path.basename(proposal.file_original_name), "wb") as f:
        f.write(base64.b64decode(download_byte))

    return proposal.file_original_name
