import os

from app.facades.database import proposals_store
from app.facades.storage import proposal_thumbnail_image
from app.schemas.proposal.domain import Proposal
from app.utils.logging import logger


def execute(proposal_id: str) -> str:
    proposal: Proposal = proposals_store.fetch_proposal(proposal_id)
    if proposal is None:  # IDに紐づく提案が存在しなければNoneを返す
        logger.warn(f"proposal is None. {proposal_id=}")
        return None

    download_byte = proposal_thumbnail_image.download(
        proposal.thumbnail_filename
    )

    with open(os.path.basename(proposal.thumbnail_filename), "wb") as f:
        f.write(download_byte)

    return proposal.thumbnail_filename
