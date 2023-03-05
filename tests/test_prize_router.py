from fastapi.testclient import TestClient

from app.facades.database import users_store
from app.main import app
from app.schemas.prize.domain import Prize
from app.schemas.prize.requests import EntryPrizeRequest
from app.schemas.prize.responses import EntryPrizeResponse
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


def test_fetch_prize(mocker):
    """景品の詳細を取得できること"""

    # give
    test_entry_prize(mocker)
    test_prize_id = "test_prize_id"
    response = client.get(
        f"/prize/{test_prize_id}",
    )

    assert response.status_code == 200
    actual_prize = Prize.parse_obj(response.json())
    assert actual_prize.name == "テスト景品"
    assert actual_prize.description == "テスト用です"
    assert actual_prize.required_token_amount == 2


def test_entry_prize_trade(mocker):
    """景品をトークンと交換できること"""
    # give
    test_entry_prize(mocker)

    test_user_id = "test_user_id"
    test_prize_id = "test_prize_id"

    _set_user_balance(test_user_id, 3)

    response = client.post(
        f"/prize/{test_prize_id}/trade",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual = response.json().get("balance")
    assert actual == 1


def test_entry_prize_trade_missing(mocker):
    """残高が十分でない場合、景品をトークンと交換できないこと"""
    # give
    test_entry_prize(mocker)

    test_user_id = "test_user_id"
    test_prize_id = "test_prize_id"

    _set_user_balance(test_user_id, 1)

    response = client.post(
        f"/prize/{test_prize_id}/trade",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 400


def _set_user_balance(user_id: str, balance: int):
    """テスト用に、指定したユーザの残高を変更する"""
    user = users_store.fetch_user(user_id)
    user.total_token_amount = balance
    users_store.add_user(id=user_id, content=user)
