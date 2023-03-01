from typing import List

from app.facades.database import proposals_store
from app.schemas.proposal.domain import Proposal


def execute(
    status: str | None = None,
    title: str | None = None,
    description: str | None = None,
    tag: str | None = None,
) -> List[Proposal] | None:
    proposals: List[Proposal] = proposals_store.find_proposals(
        status=status,
        title=title,
        description=description,
        tag=tag,
    )
    return proposals
