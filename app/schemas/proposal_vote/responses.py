from pydantic import BaseModel, Field


class EntryProposalVoteResponse(BaseModel):
    vote_nft_token_id: str = Field("", description="投票結果NFTのトークンID")
    reward: float = Field(0, description="獲得したトークン")
