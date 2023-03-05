from fastapi.testclient import TestClient

from app.facades.database import proposal_votes_store, users_store
from app.main import app
from app.schemas.proposal_vote.responses import (
    EntryProposalVoteResponse,
    FetchProposalVoteResponse,
)
from app.schemas.user.domain import User
from tests.proposal_routers.test_entry_proposal import test_entry_proposal

client = TestClient(app)


def add_vote_user(user_id: str):
    users_store.add_user(
        id=user_id,
        content=User(
            user_id=user_id,
            user_name="vote_user",
            wallet_address="0x999050DBCD3a7fDBcF1204201587797D1849AC97",  # テストユーザ2のウォレットアドレス
        ),
    )


def test_entry_proposal_vote(mocker):
    test_entry_proposal(mocker)
    test_vote_user_id = "test_vote_user_id"
    add_vote_user(test_vote_user_id)

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
        headers={"Authorization": test_vote_user_id},
        json={
            "judgement": True,
            "judgement_reason": "テスト",
        },
    )

    assert response.status_code == 200
    actual = EntryProposalVoteResponse.parse_obj(response.json())
    assert actual.vote_nft_token_id == "test_token_id"
    assert actual.reward == 1
    assert actual.balance == 1


def test_fetch_proposal_vote_voted_same_proposal_user(mocker):
    """自分の提案を確認した場合、自分の提案である旨が返されること"""
    test_entry_proposal_vote(mocker)
    # give
    test_user_id = "test_user_id"
    test_proposal_id = "test_proposal_id"

    response = client.get(
        f"/proposal/{test_proposal_id}/vote",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual = FetchProposalVoteResponse.parse_obj(response.json())
    assert actual.is_proposer == True
    assert actual.voted == False
    assert actual.vote_content is None


def test_fetch_proposal_vote_voted(mocker):
    """自分の提案でない提案を確認し投票済みの場合、投票内容が返ること"""
    test_entry_proposal_vote(mocker)
    test_vote_user_id = "test_vote_user_id"
    add_vote_user(test_vote_user_id)

    # give
    test_proposal_id = "test_proposal_id"

    response = client.get(
        f"/proposal/{test_proposal_id}/vote",
        headers={"Authorization": test_vote_user_id},
    )

    assert response.status_code == 200
    actual = FetchProposalVoteResponse.parse_obj(response.json())
    assert actual.is_proposer == False
    assert actual.voted == True
    assert actual.vote_content.user_id == test_vote_user_id
    assert actual.vote_content.proposal_id == test_proposal_id


def test_fetch_proposal_vote_not_voted(mocker):
    """自分の提案でない提案を確認し投票済みでない場合、その旨が返ること"""
    # give
    test_vote_user_id = "test_vote_user_id"
    add_vote_user(test_vote_user_id)

    test_proposal_id = "test_proposal_id"
    test_proposal_vote_id = "test_proposal_vote_id"
    proposal_votes_store.delete_proposal_vote(test_proposal_vote_id)

    response = client.get(
        f"/proposal/{test_proposal_id}/vote",
        headers={"Authorization": test_vote_user_id},
    )

    assert response.status_code == 200
    actual = FetchProposalVoteResponse.parse_obj(response.json())
    assert actual.is_proposer == False
    assert actual.voted == False
    assert actual.vote_content is None
