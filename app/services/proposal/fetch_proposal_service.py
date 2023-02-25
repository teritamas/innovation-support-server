from app.facades.firebase import proposals_store, users_store
from app.schemas.proposal.domain import Proposal
from app.schemas.user.domain import User


def execute(proposal_id: str) -> tuple[Proposal, User] | None:
    proposal: Proposal = proposals_store.fetch_proposal(proposal_id)
    if proposal is None:  # IDに紐づく提案が存在しなければNoneを返す
        print("proposal is None")
        return None
    user = users_store.fetch_user_from_wallet_address(
        proposal.proposer_wallet_address
    )
    if user is None:  # IDに紐づくユーザが存在しなければNoneを返す
        print(f"user is None. proposal {proposal}")
        return None
    return tuple[proposal, user]
