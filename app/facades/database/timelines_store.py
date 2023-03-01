from typing import List, Union

from google.cloud import firestore

from app.facades.database import fire_store
from app.schemas.proposal.domain import Proposal
from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.timeline.domain import Timeline
from app.utils.common import generate_id_str, timestamp_to_datetime
from app.utils.logging import logger

COLLECTION_PREFIX = "timelines"


def add_timeline(content: Proposal | ProposalVote):
    """タイムラインを新規追加する

    Args:
        content (timeline): 追加するタイムライン情報
    """

    fire_store.add(
        collection=COLLECTION_PREFIX,
        id=generate_id_str(),
        content=content.dict(),
    )


def fetch_timelines(timestamp: float | None) -> Timeline:
    timeline_ref = fire_store().collection(COLLECTION_PREFIX)

    if timestamp:
        timeline_ref = timeline_ref.where(
            "updated_at", ">", timestamp_to_datetime(timestamp)
        )

    timelines = (
        timeline_ref.order_by(
            "updated_at", direction=firestore.Query.DESCENDING
        )
        .limit(100)
        .stream()
    )

    contents: List[Union[Proposal, ProposalVote]] = []
    for timeline in timelines:
        timeline_obj = timeline.to_dict()
        if has_proposal_keys(timeline_obj):
            contents.append(Proposal.parse_obj(timeline_obj))
        elif has_proposal_vote_keys(timeline_obj):
            contents.append(ProposalVote.parse_obj(timeline_obj))
        else:
            logger.warn(f"Invalid Type. {timeline_obj=}")

    return Timeline(timelines=contents)


def has_proposal_vote_keys(timeline_obj):
    return (
        timeline_obj.get("judgement") is not None
        and timeline_obj.get("judgement_reason") is not None
    )


def has_proposal_keys(timeline_obj):
    return (
        timeline_obj.get("proposal_status") is not None
        and timeline_obj.get("title") is not None
    )
