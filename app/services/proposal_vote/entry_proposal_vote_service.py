from app.facades.database import (
    proposal_votes_store,
    proposals_store,
    users_store,
)
from app.facades.web3 import proposal_nft
from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.proposal_vote.requests import EntryProposalVoteRequest
from app.utils.common import generate_id_str
from app.utils.logging import logger


def execute(proposal_id: str, request: EntryProposalVoteRequest):
    # ユーザーが存在することを確認
    user = users_store.fetch_user(id=request.user_id)
    if user is None:
        logger.warn(f"userId is None. {request.user_id=}")

        return None

    # 提案が存在することを確認
    proposal = proposals_store.fetch_proposal(proposal_id)
    if proposal is None:
        logger.warn(f"proposal is None. {proposal_id=}")
        return None
    vote_user_wallet_address = user.wallet_address

    # TODO: 投票内容の評価でトークンの発行量を決める
    # コントラクトの投票処理
    nft_token_id = proposal_nft.vote(
        target_nft_id=proposal.nft_token_id,
        voter_address=vote_user_wallet_address,
        token_amount=10,
    )

    save_db(proposal_id, request, nft_token_id)

    return nft_token_id


def save_db(
    proposal_id: str, request: EntryProposalVoteRequest, nft_token_id: str
):
    """投票内容をDBに保存する"""
    proposal_vote_id = generate_id_str()
    proposal_vote = ProposalVote.parse_obj(request)
    proposal_vote.proposal_id = proposal_id
    proposal_vote.nft_token_id = nft_token_id
    proposal_votes_store.add_proposal_vote(proposal_vote_id, proposal_vote)
