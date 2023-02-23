from pydantic import BaseModel, Field


class EntryProposalVoteRequest(BaseModel):
    judgement: bool = Field(False, description="投票結果")
    judgement_reason: str = Field("", description="投票理由")
