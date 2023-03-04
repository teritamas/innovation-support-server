from pydantic import BaseModel, Field

from app.schemas.proposal_vote.domain import ProposalVote


class FetchProposalVoteDto(BaseModel):
    is_proposer: bool = Field(..., description="この提案の提案者の場合: true")
    voted: bool = Field(False, description="投票済みの場合: true.")
    vote_content: ProposalVote | None = Field(
        None, description="投票済みの場合、投票内容が含まれる。投票済みでない場合、None"
    )


class EntryProposalVoteDto(BaseModel):
    vote_nft_id: str = Field("")
    reword: int = Field(0)
