from typing import List

from pydantic import BaseModel

from app.schemas.proposal_vote.domain import ProposalVote


class FetchProposalVoteDto(BaseModel):
    positive_proposal_votes: List[ProposalVote]
    negative_proposal_votes: List[ProposalVote]
