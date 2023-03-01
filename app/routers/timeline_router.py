from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.auth.domain import AuthorizedClientSchema
from app.schemas.timeline.domain import Timeline
from app.schemas.timeline.responses import FetchTimelineResponse
from app.services.timeline import fetch_timeline_service
from app.utils.authorization import authenticate_key

timeline_router = APIRouter(prefix="/timeline", tags=["timeline"])


@timeline_router.get(
    "/",
    response_model=FetchTimelineResponse,
)
def fetch_timeline(
    timestamp: float | None = None,
    _: AuthorizedClientSchema = Depends(authenticate_key),
):
    """直近のアクティビティを10件取得する"""
    timeline: Timeline = fetch_timeline_service.execute(timestamp)
    return FetchTimelineResponse.parse_obj(timeline.dict())
