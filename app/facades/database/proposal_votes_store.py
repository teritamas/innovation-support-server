from typing import List

from app.facades.database import fire_store, proposals_store
from app.schemas.proposal_vote.domain import ProposalVote

COLLECTION_PREFIX = "proposals"


def add_proposal_vote(id: str, content: ProposalVote):
    """提案に投票結果を付与する

    Args:
        id (str): proposal_voteId
        content (ProposalVote): 追加する投票結果情報
    """
    proposal = proposals_store.fetch_proposal(id=id)
    proposal.votes.append(content)
    proposals_store.add_proposal(id=id, content=proposal)


def fetch_proposal_vote_by_proposal_id_and_user_id(
    proposal_id: str, user_id: str
) -> List[ProposalVote]:
    """user_idと提案Idから投票結果情報を検索する。

    Args:
        proposal_id (str): 提案ID
        user_id (str): ユーザーID

    Returns:
        List[ProposalVote]: 投票情報.存在しない場合は、空のListが帰る。
    """
    proposal = proposals_store.fetch_proposal(id=proposal_id)

    if proposal is None:
        return []

    proposal_votes = proposal.votes
    return [
        proposal_vote
        for proposal_vote in proposal_votes
        if proposal_vote.user_id == user_id
    ]


def fetch_proposal_vote_by_proposal_id(
    proposal_id: str,
) -> List[ProposalVote]:
    """提案Idから投票結果情報を検索する。

    Args:
        proposal_id (str): 提案ID

    Returns:
        List[ProposalVote]: 投票情報.存在しない場合は、空のListが帰る。
    """
    proposal = proposals_store.fetch_proposal(id=proposal_id)
    if proposal is None:
        return []

    return proposal.votes


def fetch_proposal_vote_by_user_id(
    user_id: str,
) -> List[ProposalVote]:
    """ユーザIdから投票結果情報を検索する。

    Args:
        user_id (str): ユーザId

    Returns:
        List[ProposalVote]: 投票情報.存在しない場合は、空のListが帰る。
    """
    proposals_col = fire_store().collection(COLLECTION_PREFIX).stream()

    proposal_votes: List[ProposalVote] = []

    for proposal in proposals_col:
        user_vote = fetch_proposal_vote_by_proposal_id_and_user_id(
            proposal_id=proposal.id, user_id=user_id
        )
        proposal_votes.extend(user_vote)
    return proposal_votes


def delete_proposal_vote(proposal_id: str, user_id):
    """投票内容を削除する(テストでのみ利用)"""
    proposal = proposals_store.fetch_proposal(id=proposal_id)

    if proposal is None:
        return []

    # 引数に与えられたユーザIDのみ削除して再代入する
    proposal_votes = proposal.votes
    proposal.votes = [
        proposal_vote
        for proposal_vote in proposal_votes
        if proposal_vote.user_id != user_id
    ]
    proposals_store.add_proposal(id=proposal_id, content=proposal)
