from fastapi import APIRouter

from app.facades.nlp import rule_base
from app.schemas.extension.requests import VerifyVoteEnrichmentRequest
from app.schemas.extension.responses import VerifyVoteEnrichmentResponse

extension_router = APIRouter(prefix="/extension", tags=["extension"])


@extension_router.post(
    "/vote/enrichment",
    description="投票の際に入力された文章の充実度を測定する。",
    response_model=VerifyVoteEnrichmentResponse,
)
def calculation_judgement_reason(
    request: VerifyVoteEnrichmentRequest,
):
    score = rule_base.calculation_judgement_reason(request.judgement_reason)
    return VerifyVoteEnrichmentResponse(
        judgement_reason=request.judgement_reason, score=score
    )
