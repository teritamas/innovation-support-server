from fastapi.testclient import TestClient

from app.facades.database import proposal_votes_store
from app.main import app
from app.schemas.proposal_vote.responses import EntryProposalVoteResponse
from tests.test_proposal_router import test_entry_proposal
from tests.test_user_router import test_entry_user

client = TestClient(app)


def test_entry_proposal_vote(mocker):
    test_entry_proposal(mocker)
    test_entry_user(mocker)

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
