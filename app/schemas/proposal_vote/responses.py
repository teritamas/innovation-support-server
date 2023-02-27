from pydantic import BaseModel, Field

from app.schemas.proposal_vote.domain import ProposalVote


class EntryProposalVoteResponse(BaseModel):
    vote_nft_token_id: str = Field("", description="投票結果NFTのトークンID")
    reward: float = Field(0, description="獲得したトークン")


class FetchProposalVoteResponse(BaseModel):
    voted: bool = Field(..., description="投票済みの場合: true.")
    vote_content: ProposalVote | None = Field(
        None, description="投票済みの場合、投票内容が含まれる。投票済みでない場合、None"
    )
