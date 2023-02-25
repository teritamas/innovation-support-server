from typing import List

from app.facades.firebase import proposals_store
from app.schemas.proposal.domain import Proposal
from app.schemas.proposal.responses import FindProposalResponse


def execute(
    tags: str | None = None, words: str | None = None
) -> FindProposalResponse | None:
    proposals: List[Proposal] = proposals_store.find_proposals()
    return FindProposalResponse(proposals=proposals)
