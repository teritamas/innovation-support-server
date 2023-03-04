from app.facades.database import (
    proposal_votes_store,
    proposals_store,
    timelines_store,
    users_store,
)
from app.facades.nlp import rule_base
from app.facades.web3 import proposal_nft
from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.proposal_vote.dto import EntryProposalVoteDto
from app.schemas.proposal_vote.requests import EntryProposalVoteRequest
from app.utils.common import generate_id_str
from app.utils.logging import logger


def execute(
    user_id: str, proposal_id: str, request: EntryProposalVoteRequest
) -> EntryProposalVoteDto:
    # ユーザーが存在することを確認
    user = users_store.fetch_user(id=user_id)
    if user is None:
        # authorization.pyで認証しているため、ここがNoneになることはほぼない。
        # その為Errorログを出しておく
        logger.error(f"user is none. {user_id=}")
        return None

    # 提案が存在することを確認
    proposal = proposals_store.fetch_proposal(proposal_id)
    if proposal is None:
        logger.warn(f"proposal is None. {proposal_id=}")
        return None
    vote_user_wallet_address = user.wallet_address

    # 投票内容の評価でトークンの発行量を決める
    score = rule_base.calculation_judgement_reason(request.judgement_reason)
    mint_token_amount = int(10 * score)
    logger.info(f"トークン発行. {user_id=}, {mint_token_amount=}")
    # コントラクトの投票処理
    nft_token_id = proposal_nft.vote(
        target_nft_id=proposal.nft_token_id,
        voter_address=vote_user_wallet_address,
        token_amount=mint_token_amount,
    )

    save_db(user_id, proposal_id, request, nft_token_id)

    return EntryProposalVoteDto(
        vote_nft_id=mint_token_amount, reword=mint_token_amount
    )


def save_db(
    user_id: str,
    proposal_id: str,
    request: EntryProposalVoteRequest,
    nft_token_id: str,
):
    """投票内容をDBに保存する"""
    proposal_vote_id = generate_id_str()
    proposal_vote = ProposalVote.parse_obj(request)
    proposal_vote.user_id = user_id
    proposal_vote.proposal_id = proposal_id
    proposal_vote.nft_token_id = nft_token_id
    proposal_votes_store.add_proposal_vote(proposal_vote_id, proposal_vote)
    timelines_store.add_timeline(content=proposal_vote)
