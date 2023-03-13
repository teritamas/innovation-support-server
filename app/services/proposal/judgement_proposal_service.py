from datetime import datetime, timedelta
from typing import List

from app.facades.database import proposals_store
from app.facades.web3 import proposal_vote
from app.schemas.proposal.domain import (
    JudgementStatusDto,
    Proposal,
    ProposalFundraisingCondition,
    ProposalStatus,
)
from app.schemas.proposal_vote.domain import ProposalVote
from app.utils.common import now
from app.utils.logging import logger


async def execute(proposal_id: str) -> JudgementStatusDto:
    """提案の状態を確認し、可決しているかどうかを確認する。"""

    proposal: Proposal = proposals_store.fetch_proposal(id=proposal_id)
    if proposal is None:
        RuntimeError

    condition: ProposalFundraisingCondition = (
        proposal.proposal_fundraising_condition
    )

    # 締切を過ぎていない場合は、その場で返す
    if not _past_limit_date(proposal.created_at, condition.limit_date):
        proposals_store.update_proposal(
            id=proposal_id, status=ProposalStatus.VOTING
        )
        return JudgementStatusDto(
            proposal_status=ProposalStatus.VOTING,
            is_limit=False,
            fill_min_voter_count=False,
            fill_min_agreement_count=False,
        )

    # 締切を過ぎている場合は、各種要素で判断していく
    # 最低得票数を満たしている
    fill_min_voter_count = _check_fill_min_voter_count(
        proposal.votes, condition.min_voter_count
    )
    # 最低賛成者数を満たしている
    fill_min_agreement_count = _check_fill_min_agreement_count(
        proposal.votes,
        int(condition.min_voter_count * condition.min_agreement_count),
    )

    judgement_result = fill_min_voter_count and fill_min_agreement_count
    result_proposal_status = (
        ProposalStatus.ACCEPT if judgement_result else ProposalStatus.REJECT
    )

    # コントラクトをアップデートする
    try:
        await proposal_vote.judgement_proposal(
            tokenId=int(proposal.nft_token_id), judgement=judgement_result
        )
    except Exception as e:
        logger.warning(f"コントラクト上の承認処理で失敗しました。{e=}")

    # DBの内容を更新する
    proposals_store.update_proposal(
        id=proposal_id, status=result_proposal_status
    )

    return JudgementStatusDto(
        proposal_status=result_proposal_status,
        is_limit=True,  # 必ずTrueになる
        fill_min_voter_count=fill_min_voter_count,
        fill_min_agreement_count=fill_min_agreement_count,
    )


def _past_limit_date(start_datetime: datetime, limit_date: int) -> bool:
    """現在の日付が投票締切を超えている場合trueを返す"""
    limit_datetime = start_datetime + timedelta(days=limit_date)
    return limit_datetime < now()


def _check_fill_min_voter_count(
    votes: List[ProposalVote], min_voter_count: int
):
    """投票者が最低投票人数を超えている場合trueを返す"""
    return len(votes) >= min_voter_count


def _check_fill_min_agreement_count(
    votes: List[ProposalVote], min_agreement_count: int
):
    """賛成者が最低賛成人数を超えている場合trueを返す"""
    agreement_votes = [v for v in votes if v.judgement]
    return len(agreement_votes) >= min_agreement_count
