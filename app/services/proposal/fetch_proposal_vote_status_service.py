from typing import List

from app.facades.database import proposal_votes_store, proposals_store
from app.schemas.proposal.domain import Proposal
from app.schemas.proposal.dto import FetchProposalVoteDto
from app.schemas.proposal_vote.domain import ProposalVote


def execute(user_id: str, proposal_id: str) -> FetchProposalVoteDto | None:
    if not _is_status_accessible_user(user_id, proposal_id):
        return None

    # 投票結果を集計する
    proposal_votes = proposal_votes_store.fetch_proposal_vote_by_proposal_id(
        proposal_id=proposal_id
    )

    positive_proposal_votes: List[ProposalVote] = []
    negative_proposal_votes: List[ProposalVote] = []

    for proposal_vote in proposal_votes:
        if proposal_vote.judgement:
            positive_proposal_votes.append(proposal_vote)
        else:
            negative_proposal_votes.append(proposal_vote)

    return FetchProposalVoteDto(
        positive_proposal_votes=positive_proposal_votes,
        negative_proposal_votes=negative_proposal_votes,
    )


def _is_status_accessible_user(user_id: str, proposal_id: str) -> bool:
    """ユーザが、投票ステータスにアクセス可能な状態かを判別する。"""
    # ユーザが投票済みかどうかを確認する
    my_proposal_vote = (
        proposal_votes_store.fetch_proposal_vote_by_proposal_id_and_user_id(
            proposal_id=proposal_id, user_id=user_id
        )
    )
    if my_proposal_vote == []:  # 投票していない
        proposal: Proposal = proposals_store.fetch_proposal(proposal_id)
        if proposal.user_id != user_id:  # 投票しておらず、対象の提案者でない場合
            return False

    return True
