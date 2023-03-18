from app import config
from app.facades.database import proposals_store, users_store
from app.facades.web3 import proposal_vote
from app.schemas.proposal.domain import Proposal
from app.schemas.proposal.dto import ProposalDetailDto
from app.schemas.proposal_vote.domain import ProposalVoteOnContract
from app.schemas.user.domain import User
from app.utils.logging import logger


def execute(proposal_id: str) -> tuple[ProposalDetailDto, User] | None:
    proposal: Proposal = proposals_store.fetch_proposal(proposal_id)
    if proposal is None:  # IDに紐づく提案が存在しなければNoneを返す
        logger.warn(f"proposal is none. {proposal_id}")
        return None

    proposal_dto = _build_proposal_dto(proposal)

    user = users_store.fetch_user(proposal.user_id)
    if user is None:  # IDに紐づくユーザが存在しなければNoneを返す
        logger.warn(f"user is none. {proposal=}")
        return None

    ## TODO: 詳細取得時に条件を満たしていれば、クローズにする
    return (proposal_dto, user)


def _build_proposal_dto(proposal):
    proposal_dto = ProposalDetailDto.parse_obj(proposal.dict())
    block_explorer_url = f"{config.block_explorer_url}/token/{config.proposal_nft_contract_address}?a={proposal.nft_token_id}"
    proposal_dto.block_explorer_url_path = block_explorer_url
    return proposal_dto
