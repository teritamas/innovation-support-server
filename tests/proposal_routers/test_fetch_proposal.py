from fastapi.testclient import TestClient

from app.facades.database import proposal_votes_store, users_store
from app.main import app
from app.schemas.proposal.domain import Proposal
from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.user.domain import User
from tests.proposal_routers.test_entry_proposal import test_entry_proposal

client = TestClient(app)


def test_fetch_proposal(mocker):
    """IDから提案内容を取得できること"""
    test_entry_proposal(mocker)
    # give
    test_user_id = "test_user_id"
    test_proposal_id = "test_proposal_id"
    response = client.get(
        f"/proposal/{test_proposal_id}",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual_proposal = Proposal.parse_obj(response.json().get("proposal"))
    assert actual_proposal.proposal_id == test_proposal_id
    actual_user = User.parse_obj(response.json().get("proposal_user"))
    assert actual_user.user_id == "test_user_id"


def test_fetch_proposal_vote_status(mocker):
    """提案に対する投票状態を返す"""
    test_entry_proposal(mocker)

    # give
    test_proposal_id = "test_proposal_id"
    positive_user_count = 10
    negative_user_count = 5

    _add_test_votes(
        test_proposal_id=test_proposal_id,
        positive_user_count=positive_user_count,
        negative_user_count=negative_user_count,
    )
    test_user_id = "positive_user_0"  # positiveの一人目は必ず存在するので、このユーザをテストユーザとする

    # when
    response = client.get(
        f"/proposal/{test_proposal_id}/vote_status",
        headers={"Authorization": test_user_id},
    )

    # then
    assert response.status_code == 200
    assert response.json().get("vote_action") == False
    actual_positive_votes = response.json().get("positive_proposal_votes")
    assert len(actual_positive_votes) == positive_user_count
    actual_negative_votes = response.json().get("negative_proposal_votes")
    assert len(actual_negative_votes) == negative_user_count


def test_fetch_proposal_vote_status_not_voted_not_proposer(mocker):
    """投票していないくて提案者でない場合、提案に対する投票状態を返さないこと"""
    test_entry_proposal(mocker)

    # give
    test_proposal_id = "test_proposal_id"
    positive_user_count = 10
    negative_user_count = 5

    _add_test_votes(
        test_proposal_id=test_proposal_id,
        positive_user_count=positive_user_count,
        negative_user_count=negative_user_count,
    )
    test_user_id = "test_vote_user_id"  # 提案者でないユーザのユーザID
    _add_vote_user(test_user_id)

    # when
    response = client.get(
        f"/proposal/{test_proposal_id}/vote_status",
        headers={"Authorization": test_user_id},
    )

    # then
    assert response.status_code == 200
    assert response.json().get("vote_action") == True
    actual_positive_votes = response.json().get("positive_proposal_votes")
    assert len(actual_positive_votes) == 0
    actual_negative_votes = response.json().get("negative_proposal_votes")
    assert len(actual_negative_votes) == 0


def test_fetch_proposal_vote_status_not_voted_proposer(mocker):
    """投票していないくて提案者の場合、提案に対する投票状態を返すこと"""
    test_entry_proposal(mocker)

    # give
    test_proposal_id = "test_proposal_id"
    positive_user_count = 10
    negative_user_count = 5

    _add_test_votes(
        test_proposal_id=test_proposal_id,
        positive_user_count=positive_user_count,
        negative_user_count=negative_user_count,
    )
    test_user_id = "test_user_id"  # 提案者のユーザID
    _add_vote_user(test_user_id)

    # when
    response = client.get(
        f"/proposal/{test_proposal_id}/vote_status",
        headers={"Authorization": test_user_id},
    )

    # then
    assert response.status_code == 200
    assert response.json().get("vote_action") == False
    actual_positive_votes = response.json().get("positive_proposal_votes")
    assert len(actual_positive_votes) == positive_user_count
    actual_negative_votes = response.json().get("negative_proposal_votes")
    assert len(actual_negative_votes) == negative_user_count


def _add_test_votes(
    test_proposal_id: str, positive_user_count: int, negative_user_count: int
):
    for i in range(positive_user_count):
        _add_user(test_proposal_id, i, judgement=True, prefix="positive")
    for i in range(negative_user_count):
        _add_user(test_proposal_id, i, judgement=False, prefix="negative")


def _add_user(test_proposal_id, index, judgement: bool, prefix: str = ""):
    user_id = f"{prefix}_user_{index}"
    users_store.add_user(
        id=user_id,
        content=User(
            user_id=user_id,
            user_name=f"{prefix}_vote_user_{index}",
            wallet_address="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",  # テストユーザ2のウォレットアドレス
        ),
    )

    proposal_votes_store.add_proposal_vote(
        f"{prefix}_vote_{index}",
        ProposalVote(
            proposal_id=test_proposal_id,
            user_id=user_id,
            judgement=judgement,
            judgement_reason=f"{prefix} vote no {index}",
        ),
    )


def _add_vote_user(user_id: str):
    users_store.add_user(
        id=user_id,
        content=User(
            user_id=user_id,
            user_name="vote_user",
            wallet_address="0x999050DBCD3a7fDBcF1204201587797D1849AC97",  # テストユーザ2のウォレットアドレス
        ),
    )
