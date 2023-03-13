from fastapi import APIRouter

from app.schemas.extension.dto import VerifyVoteEnrichmentDto
from app.schemas.extension.requests import VerifyVoteEnrichmentRequest
from app.schemas.extension.responses import VerifyVoteEnrichmentResponse
from app.services.extension import calculation_judgement_reason_service

extension_router = APIRouter(prefix="/extension", tags=["extension"])


@extension_router.post(
    "/vote/enrichment",
    description="投票の際に入力された文章の充実度を測定する。",
    response_model=VerifyVoteEnrichmentResponse,
)
def calculation_judgement_reason(
    request: VerifyVoteEnrichmentRequest,
):
    dto: VerifyVoteEnrichmentDto = (
        calculation_judgement_reason_service.execute(request.judgement_reason)
    )

    response = VerifyVoteEnrichmentResponse.parse_obj(dto.dict())
    response.judgement_reason = request.judgement_reason
    return response
