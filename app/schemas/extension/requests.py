from pydantic import BaseModel, Field


class VerifyVoteEnrichmentRequest(BaseModel):
    judgement_reason: str = Field("", description="投票理由")
