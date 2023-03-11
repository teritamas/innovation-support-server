from fastapi.testclient import TestClient

from app.main import app
from app.schemas.user.response import DetailUserResponse
from tests.test_account_router import test_signup_not_exists
from tests.test_proposal_vote_router import test_entry_proposal_vote

client = TestClient(app)


def test_fetch_user(mocker):
    test_signup_not_exists(mocker)
    # give
    test_user_id = "test_user_id"
    mocker.patch(  # test_signup_not_existsではトークン量を0で登録し、実際のトークン量=10で更新されることを確認する
        "app.services.user.detail_user_service.inosapo_ft.balance_of_address",
        return_value=10,
    )
    response = client.get(
        f"/user/{test_user_id}",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual_user = DetailUserResponse.parse_obj(response.json())
    assert actual_user.user_id == test_user_id
    # assert actual_user.total_token_amount == 0  # TODO: 状況に応じて減ったり増えたりするのでコメントアウト
    assert actual_user.user_name == "test_user"
    assert actual_user.message == ""
    assert (
        actual_user.wallet_address
        == "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"
    )
    assert len(actual_user.proposal_votes) == 0


def test_fetch_voted_user(mocker):
    """投票したユーザの情報が取得できること"""
    test_signup_not_exists(mocker)
    test_entry_proposal_vote(mocker)

    # give
    test_user_id = "test_vote_user_id"

    response = client.get(
        f"/user/{test_user_id}",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual_user = DetailUserResponse.parse_obj(response.json())
    assert actual_user.user_id == test_user_id
    # assert actual_user.total_token_amount == 10  # 投票しているので10
    assert actual_user.user_name == "vote_user"
    assert actual_user.message == ""
    assert (
        actual_user.wallet_address
        == "0x999050DBCD3a7fDBcF1204201587797D1849AC97"
    )
    assert len(actual_user.proposals) == 0
    assert len(actual_user.proposal_votes) == 1
    assert actual_user.proposal_votes[0].judgement == True
    assert actual_user.proposal_votes[0].judgement_reason == "テスト"
