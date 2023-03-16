from app.facades.database import (
    proposal_votes_store,
    proposals_store,
    timelines_store,
    users_store,
)
from app.facades.nlp import rule_base
from app.facades.web3 import inosapo_ft, proposal_vote
from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.proposal_vote.dto import EntryProposalVoteDto
from app.schemas.proposal_vote.requests import EntryProposalVoteRequest
from app.schemas.user.domain import AccountType
from app.utils.common import generate_id_str, now
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

    if user.account_type == AccountType.STANDARD:
        _mint_token_on_blockchain(request, user, proposal, mint_token_amount)
    else:
        # 一時ユーザの場合はmintせず、一時領域に保管する
        users_store.add_cached_token_amount(
            user_id=user_id, amount=mint_token_amount
        )

    save_db(user_id, proposal_id, request, "", mint_token_amount)
    balance = users_store.add_token_amount(
        user_id=user_id, amount=mint_token_amount
    )

    return EntryProposalVoteDto(
        vote_nft_id="", reword=mint_token_amount, balance=balance
    )


def _mint_token_on_blockchain(request, user, proposal, mint_token_amount):
    logger.info(f"トークン発行. {user.user_id=}, {mint_token_amount=}")
    try:
        # TODO: スマコンでトークンの送金までできるようにする。
        proposal_vote.vote(
            int(proposal.nft_token_id), user.wallet_address, request.judgement
        )
        inosapo_ft.transfer(user.wallet_address, amount=mint_token_amount)
    except Exception as e:
        logger.warn(f"コントラクトの実行処理で失敗しました.投票処理は完了させます.  {e=}")


def save_db(
    user_id: str,
    proposal_id: str,
    request: EntryProposalVoteRequest,
    nft_token_id: str,
    mint_token_amount: int,
):
    """投票内容をDBに保存する"""
    proposal_vote = ProposalVote.parse_obj(request)
    proposal_vote.user_id = user_id
    proposal_vote.mint_token_amount = mint_token_amount
    proposal_vote.created_at = now()
    proposal_vote.updated_at = now()
    proposal_votes_store.add_proposal_vote(proposal_id, proposal_vote)
    timelines_store.add_timeline(content=proposal_vote)
