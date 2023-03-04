from typing import List

from pydantic import BaseModel, Field

from app.schemas.proposal.domain import Proposal
from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.user.domain import User


class DetailUserDto(User):
    proposals: List[Proposal] = Field([Proposal()], description="ユーザが実施した提案一覧")
    proposal_votes: List[ProposalVote] = Field(
        [ProposalVote()], description="ユーザが実施した投票一覧"
    )
