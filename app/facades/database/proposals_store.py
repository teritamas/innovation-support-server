from typing import List

from app.facades.database import fire_store
from app.schemas.proposal.domain import Proposal

COLLECTION_PREFIX = "proposals"


def add_proposal(id: str, content: Proposal):
    """提案内容を新規追加する

    Args:
        id (str): ProposalId
        content (Proposal): 追加する提案情報
    """
    fire_store.add(collection=COLLECTION_PREFIX, id=id, content=content.dict())


def fetch_proposal(id: str) -> Proposal:
    """提案内容を検索する

    Args:
        id (str): ProposalId
    """
    return Proposal.parse_obj(
        fire_store.fetch(collection=COLLECTION_PREFIX, id=id)
    )


def find_proposals(
    proposal_status: str | None = None,
    title: str | None = None,
    description: str | None = None,
    tag: str | None = None,
) -> List[Proposal]:
    """提案内容を全て検索する"""
    proposals_ref = fire_store().collection(COLLECTION_PREFIX)

    if proposal_status:
        proposals_ref = proposals_ref.where(
            "proposal_status", "==", proposal_status
        )
    if tag:
        proposals_ref = proposals_ref.where("tags", "array_contains", tag)

    proposals = proposals_ref.stream()
    proposals_list = [
        Proposal.parse_obj(proposal.to_dict()) for proposal in proposals
    ]

    if title:
        proposals_list = list(
            filter(lambda x: title in x.title, proposals_list)
        )

    if description:
        proposals_list = list(
            filter(lambda x: description in x.description, proposals_list)
        )

    return proposals_list


def delete_proposal(id: str):
    fire_store.delete(collection=COLLECTION_PREFIX, id=id)
