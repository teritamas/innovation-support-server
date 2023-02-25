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


def find_proposals() -> List[Proposal]:
    """提案内容を全て検索する"""
    proposals = fire_store().collection(COLLECTION_PREFIX).stream()
    return [Proposal.parse_obj(proposal.to_dict()) for proposal in proposals]


def delete_proposal(id: str):
    fire_store.delete(collection=COLLECTION_PREFIX, id=id)
