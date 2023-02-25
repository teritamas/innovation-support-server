from app.facades.firebase import proposals_store, users_store
from app.schemas.proposal_vote.requests import EntryProposalVoteRequest
from app.schemas.proposal_vote.responses import EntryProposalVoteResponse


def execute(proposal_id: str, request: EntryProposalVoteRequest):
    user = users_store.fetch_user(id=request.user_id)
    if user is None:
        return None

    proposal = proposals_store.fetch_proposal(proposal_id)
    if proposal is None:
        return None
    vote_user_wallet_address = user.wallet_address

    # TODO: 投票内容の評価でトークンの発行量を決める
    # TODO: ここでコントラクトの投票処理

    return "temp_nft_id"
