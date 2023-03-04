from fastapi.testclient import TestClient

from app.main import app
from app.schemas.prize.requests import EntryPrizeRequest
from app.schemas.prize.responses import EntryPrizeResponse
from app.schemas.user.domain import User
from tests.test_account_router import test_signup_not_exists

client = TestClient(app)


def test_entry_prize(mocker):
    """景品を登録できること"""
    test_signup_not_exists(mocker)
    # give
    test_user_id = "test_user_id"
    test_prize_id = "test_prize_id"
    mocker.patch(
        "app.services.prize.entry_prize_service.generate_id_str",
        return_value=test_prize_id,
    )
    request = EntryPrizeRequest(
        name="テスト景品",
        description="テスト用です",
        required_token_amount=2,
        recommendation_score=3,
    )

    response = client.post(
        f"/prize", headers={"Authorization": test_user_id}, data=request.json()
    )

    assert response.status_code == 200
    actual = EntryPrizeResponse.parse_obj(response.json())

    assert actual.prize_id == test_prize_id


def test_find_prize(mocker):
    """景品の一覧を取得できること"""

    # give
    test_entry_prize(mocker)
    response = client.get(
        f"/prize",
    )

    assert response.status_code == 200
    actual = response.json().get("prizes")
    assert type(actual) == list
    assert actual[0].get("name") == "テスト景品"
