from fastapi.testclient import TestClient

from app.facades.database import proposal_votes_store
from app.main import app
from app.schemas.proposal_vote.responses import (
    EntryProposalVoteResponse,
    FetchProposalVoteResponse,
)
from tests.test_proposal_router import test_entry_proposal
from tests.test_user_router import test_entry_user_not_exists

client = TestClient(app)


def test_entry_proposal_vote(mocker):
    test_entry_proposal(mocker)
    test_entry_user_not_exists(mocker)

    # give
    test_proposal_vote_id = "test_proposal_vote_id"
    test_proposal_id = "test_proposal_id"
    test_token_id = "test_token_id"
    mocker.patch(
        "app.services.proposal_vote.entry_proposal_vote_service.generate_id_str",
        return_value=test_proposal_vote_id,
    )
    mocker.patch(
        "app.services.proposal_vote.entry_proposal_vote_service.proposal_nft.vote",
        return_value=test_token_id,
    )
    proposal_votes_store.delete_proposal_vote(test_proposal_vote_id)

    response = client.post(
        f"/proposal/{test_proposal_id}/vote",
        json={
            "user_id": "test_uuid",
            "judgement": True,
            "judgement_reason": "テスト",
        },
    )

    assert response.status_code == 200
    actual = EntryProposalVoteResponse.parse_obj(response.json())
    assert actual.vote_nft_token_id == "test_token_id"


def test_fetch_proposal_vote_voted(mocker):
    """投票済みの場合、投票内容が返ること"""
    test_entry_proposal_vote(mocker)
    # give
    test_user_id = "test_uuid"
    test_proposal_id = "test_proposal_id"

    response = client.get(
        f"/proposal/{test_proposal_id}/vote/{test_user_id}",
    )

    assert response.status_code == 200
    actual = FetchProposalVoteResponse.parse_obj(response.json())
    assert actual.voted == True
    assert actual.vote_content.user_id == test_user_id
    assert actual.vote_content.proposal_id == test_proposal_id


def test_fetch_proposal_vote_not_voted():
    """投票済みでない場合"""
    # give
    not_voted_test_user_id = "not_voted_test_uuid"
    test_proposal_id = "test_proposal_id"

    response = client.get(
        f"/proposal/{test_proposal_id}/vote/{not_voted_test_user_id}",
    )

    assert response.status_code == 200
    actual = FetchProposalVoteResponse.parse_obj(response.json())
    assert actual.voted == False
    assert actual.vote_content is None
