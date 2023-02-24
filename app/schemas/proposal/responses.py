from typing import List
from pydantic import BaseModel, Field, PositiveInt

from app.schemas.proposal.domain import Proposal
from ..user.domain import User


class EntryProposalResponse(BaseModel):
    proposal_id: str = Field("", description="提案ID")


class DetailProposalResponse(BaseModel):
    proposal: Proposal = Field(Proposal(), descriptions="提案内容")
    proposal_user: User = Field(User(), descriptions="ユーザ情報")


class FindProposalResponse(BaseModel):
    proposals: List[Proposal] = Field([Proposal()], descriptions="提案内容")
