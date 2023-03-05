from pydantic import BaseModel, Field

from app.schemas.proposal_vote.domain import ProposalVote


class EntryProposalVoteResponse(BaseModel):
    vote_nft_token_id: str = Field("", description="投票結果NFTのトークンID")
    reward: float = Field(0, description="獲得したトークン")
    balance: int = Field(0, description="計算後の保有トークン量")


class FetchProposalVoteResponse(BaseModel):
    is_proposer: bool = Field(..., description="この提案の提案者の場合: true")
    voted: bool = Field(..., description="投票済みの場合: true.")
    vote_content: ProposalVote | None = Field(
        None, description="投票済みの場合、投票内容が含まれる。投票済みでない場合、None"
    )
