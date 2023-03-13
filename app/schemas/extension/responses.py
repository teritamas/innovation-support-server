from pydantic import Field

from app.schemas.extension.dto import VerifyVoteEnrichmentDto


class VerifyVoteEnrichmentResponse(VerifyVoteEnrichmentDto):
    judgement_reason: str = Field("", description="入力された投票理由")
