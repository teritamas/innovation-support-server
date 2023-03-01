from app.facades.database import timelines_store
from app.schemas.timeline.domain import Timeline


def execute(timestamp: float) -> Timeline:
    return timelines_store.fetch_timelines(timestamp=timestamp)
