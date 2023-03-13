from typing import List

from pydantic import BaseModel, Field

from app.schemas.proposal.domain import Proposal
from app.schemas.proposal.dto import ListProposalDto
from app.schemas.proposal_vote.domain import ProposalVote

from ..user.domain import User


class EntryProposalResponse(BaseModel):
    proposal_id: str = Field("", description="提案ID")


class DetailProposalResponse(BaseModel):
    proposal: Proposal = Field(Proposal(), description="提案内容")
    proposal_user: User = Field(User(), description="ユーザ情報")


class FindProposalResponse(BaseModel):
    proposals: List[ListProposalDto] = Field(
        [ListProposalDto()], description="提案内容一覧"
    )


class FetchVoteStatusResponse(BaseModel):
    vote_action: bool = Field(
        False,
        description="投票が必要であればTrueとなる. その場合、positive_proposal_votesとnegative_proposal_votesは空",
    )
    positive_proposal_votes: List[ProposalVote] = Field(
        [ProposalVote()], description="賛成意見. vote_action=Trueの時は空"
    )
    negative_proposal_votes: List[ProposalVote] = Field(
        [ProposalVote()], description="反対意見. vote_action=Trueの時は空"
    )
