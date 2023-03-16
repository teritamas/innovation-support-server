from typing import List

from pydantic import BaseModel, Field

from app.schemas.proposal.domain import Proposal
from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.user.domain import User


class EntryUserService(BaseModel):
    user_id: str = Field(
        ...,
    )
    account_type: str = Field(
        ...,
    )


class UserProposalVote(ProposalVote):
    proposal_id: str = Field("abcdefg", max_length=256, description="提案ID")
    title: str = Field("タイトルサンプル", max_length=256, description="提案のタイトル")


class DetailUserDto(User):
    proposals: List[Proposal] = Field([Proposal()], description="ユーザが実施した提案一覧")
    proposal_votes: List[UserProposalVote] = Field(
        [], description="ユーザが実施した投票一覧"
    )
