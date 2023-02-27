from typing import List

from app.facades.database import fire_store
from app.schemas.proposal_vote.domain import ProposalVote

COLLECTION_PREFIX = "proposal_votes"


def add_proposal_vote(id: str, content: ProposalVote):
    """投票結果を新規追加する

    Args:
        id (str): proposal_voteId
        content (ProposalVote): 追加する投票結果情報
    """
    fire_store.add(collection=COLLECTION_PREFIX, id=id, content=content.dict())


def fetch_proposal_vote(id: str) -> ProposalVote | None:
    """idから投票結果情報を検索する。

    Args:
        id (str): 投票結果情報

    Returns:
        ProposalVote | None:
    """
    proposal_vote_dict = fire_store.fetch(collection=COLLECTION_PREFIX, id=id)
    return (
        ProposalVote.parse_obj(proposal_vote_dict)
        if proposal_vote_dict
        else None
    )


def delete_proposal_vote(id: str):
    fire_store.delete(collection=COLLECTION_PREFIX, id=id)
