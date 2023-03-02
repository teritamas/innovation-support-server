from pydantic import BaseModel, Field


class VerifyVoteEnrichmentResponse(BaseModel):
    judgement_reason: str = Field("", description="入力された投票理由")
    score: float = Field(0, description="スコア")
