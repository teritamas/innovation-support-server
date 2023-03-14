import sys

from fastapi import APIRouter

sys.path.append("../")
from app.facades.database import proposals_store
from scripts import sample_vote

demo_router = APIRouter(prefix="/demo", tags=["demo"])


@demo_router.post(
    "/{proposal_id}",
    description="提案を強制的に可決.",
)
def force_accept_proposal(proposal_id: str):
    proposal = proposals_store.fetch_proposal(id=proposal_id)

    sample_vote.main(
        proposal_id,
        voter_count=proposal.proposal_fundraising_condition.min_voter_count,
        agreement_rate=proposal.proposal_fundraising_condition.min_agreement_count,
        is_complete_vote=True,  # 自動で１年前の日付にする処理を外す
    )
