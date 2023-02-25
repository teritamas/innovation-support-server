from app.facades.firebase import proposals_store, users_store
from app.facades.web3 import proposal_nft
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
    # コントラクトの投票処理
    proposal_nft.vote(
        target_nft_id=proposal.nft_token_id,
        voter_address=vote_user_wallet_address,
        token_amount=10,
    )

    return "temp_nft_id"
