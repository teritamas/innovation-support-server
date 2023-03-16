from typing import List

from pydantic import BaseModel, Field

from app.schemas.proposal.domain import Proposal
from app.schemas.user.domain import User
from app.schemas.user.dto import UserProposalVote


class EntryUserResponse(BaseModel):
    user_id: str = Field("", description="ユーザID")
    account_type: str = Field("", description="アカウントの種類")


class UpdateStandardUserResponse(BaseModel):
    user_id: str = Field("", description="ユーザID")
    account_type: str = Field("", description="アカウントの種類")


class DetailUserResponse(User):
    proposals: List[Proposal] = Field([Proposal()], description="ユーザが実施した提案一覧")
    proposal_votes: List[UserProposalVote] = Field(
        [], description="ユーザが実施した投票一覧"
    )
