from typing import List

from app.facades.database import proposal_votes_store, proposals_store
from app.schemas.proposal.domain import Proposal, ProposalOwnType
from app.schemas.proposal.dto import ListProposalDto
from app.schemas.proposal_vote.domain import ProposalVote


def execute(
    user_id: str | None = None,
    proposal_status: str | None = None,
    title: str | None = None,
    description: str | None = None,
    tag: str | None = None,
) -> List[ListProposalDto] | None:
    proposals: List[Proposal] = proposals_store.find_proposals(
        proposal_status=proposal_status,
        title=title,
        description=description,
        tag=tag,
    )
    responses = []
    for proposal in proposals:
        list_proposal_dto = ListProposalDto.parse_obj(proposal.dict())
        if user_id is None:
            list_proposal_dto.proposal_own_type = ProposalOwnType.UNKNOWN
        elif user_id == proposal.user_id:
            list_proposal_dto.proposal_own_type = ProposalOwnType.OWNER
        elif _user_voted(proposal_id=proposal.proposal_id, user_id=user_id):
            list_proposal_dto.proposal_own_type = ProposalOwnType.VOTED
        else:
            list_proposal_dto.proposal_own_type = ProposalOwnType.UNVOTED

        responses.append(list_proposal_dto)

    return responses


def _user_voted(proposal_id: str, user_id: str):
    """ユーザが投票済みの場合Trueを返す"""
    my_proposal_vote = (
        proposal_votes_store.fetch_proposal_vote_by_proposal_id_and_user_id(
            proposal_id=proposal_id, user_id=user_id
        )
    )
    if my_proposal_vote != []:  # 投票した場合アクセス可能
        return True
    else:
        return False
