from typing import List

from pydantic import BaseModel, Field

from app.schemas.proposal.domain import Proposal, ProposalOwnType
from app.schemas.proposal_vote.domain import ProposalVote


class FetchProposalVoteDto(BaseModel):
    positive_proposal_votes: List[ProposalVote]
    negative_proposal_votes: List[ProposalVote]


class ListProposalDto(Proposal):
    proposal_own_type: ProposalOwnType = Field(
        ProposalOwnType.UNKNOWN, description="ユーザにとっての一覧に含まれる提案の所有タイプ"
    )
