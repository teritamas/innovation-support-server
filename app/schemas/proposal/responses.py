from lib2to3.pytree import Base
from typing import List

from fastapi import File
from pydantic import BaseModel, Field

from app.schemas.proposal.domain import Proposal

from ..user.domain import User


class EntryProposalResponse(BaseModel):
    proposal_id: str = Field("", description="提案ID")


class DetailProposalResponse(BaseModel):
    proposal: Proposal = Field(Proposal(), descriptions="提案内容")
    proposal_user: User = Field(User(), descriptions="ユーザ情報")


class FindProposalResponse(BaseModel):
    proposals: List[Proposal] = Field([Proposal()], descriptions="提案内容一覧")
