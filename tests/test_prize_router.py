import pytest
from fastapi.testclient import TestClient

from app.facades.database import prizes_store, users_store
from app.main import app
from app.schemas.prize.domain import Prize
from app.schemas.prize.requests import EntryPrizeRequest
from app.schemas.prize.responses import EntryPrizeResponse
from tests.test_account_router import test_signup_not_exists

client = TestClient(app)


def test_entry_prize(mocker):
    """研修の景品を登録できること"""
    test_signup_not_exists(mocker)
    # give
    test_user_id = "test_user_id"
    test_prize_id = "test_training_prize_id"
    mocker.patch(
        "app.services.prize.entry_prize_service.generate_id_str",
        return_value=test_prize_id,
    )
    request = EntryPrizeRequest(
        name="[テスト]研修A",
        description="E2E試験で自動作成されたコンテンツです",
        required_token_amount=2,
        recommendation_score=3,
        type="Training",
    )

    response = client.post(
        f"/prize", headers={"Authorization": test_user_id}, data=request.json()
    )

    assert response.status_code == 200
    actual = EntryPrizeResponse.parse_obj(response.json())

    assert actual.prize_id == test_prize_id


@pytest.mark.skipif(True, reason="サンプルテスト登録用のテストコードのため")
def test_entry_prize_for_sample(mocker):
    """研修の景品を登録できること"""
    test_signup_not_exists(mocker)
    # give
    test_user_id = "test_user_id"

    response = _insert_request(
        test_user_id,
        name="プロジェクトマネジメント入門: 企画から納品までの基礎知識",
        description="プロジェクトマネジメントの基礎知識を学び、プロジェクトの企画、実行、納品までのプロセスを理解する研修。",
        required_token_amount=10,
        recommendation_score=3,
    )
    response = _insert_request(
        test_user_id,
        name="ビジネスプレゼンテーション: 魅力的なプレゼン資料の作成とスピーチの技法",
        description="効果的なプレゼンテーションの作成方法と、プレゼンテーションの際に必要なスキルを学ぶ研修。",
        required_token_amount=5,
        recommendation_score=4,
    )
    response = _insert_request(
        test_user_id,
        name="マーケティング戦略: 顧客との接点を最大限に活用する方法",
        description="マーケティング戦略の基礎知識と、顧客との接点を最大限に活用するための戦略を学ぶ研修。",
        required_token_amount=10,
        recommendation_score=4,
    )

    response = _insert_request(
        test_user_id,
        name="データ分析入門: ExcelとGoogleスプレッドシートを使ったデータの分析方法",
        description="ExcelやGoogleスプレッドシートを使ったデータの分析方法を学び、ビジネス上でデータを活用するためのスキルを身につける研修。",
        required_token_amount=10,
        recommendation_score=5,
    )
    response = _insert_request(
        test_user_id,
        name="コミュニケーションスキル: 効果的なコミュニケーションの基礎",
        description="コミュニケーションスキルの基礎知識を学び、ビジネス上でのコミュニケーション能力を向上させるための研修。",
        required_token_amount=12,
        recommendation_score=5,
    )

    assert response.status_code == 200
    actual = EntryPrizeResponse.parse_obj(response.json())


def _insert_request(
    test_user_id,
    name,
    description,
    required_token_amount,
    recommendation_score,
):
    request = EntryPrizeRequest(
        name=name,
        description=description,
        required_token_amount=required_token_amount,
        recommendation_score=recommendation_score,
        type="Training",
    )

    response = client.post(
        f"/prize", headers={"Authorization": test_user_id}, data=request.json()
    )

    return response


def test_entry_prize_welfare(mocker):
    """休息の景品を登録できること"""
    test_signup_not_exists(mocker)
    # give
    test_user_id = "test_user_id"
    test_prize_id = "test_welfare_prize_id"
    mocker.patch(
        "app.services.prize.entry_prize_service.generate_id_str",
        return_value=test_prize_id,
    )
    request = EntryPrizeRequest(
        name="[テスト]休息A",
        description="E2E試験で自動作成されたコンテンツです",
        required_token_amount=2,
        recommendation_score=3,
        type="Welfare",
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
    test_entry_prize_welfare(mocker)
    response = client.get(
        f"/prize",
    )

    assert response.status_code == 200
    actual = response.json().get("prizes")
    assert type(actual) == list
    training = [
        a for a in actual if a.get("prize_id") == "test_training_prize_id"
    ][0]
    assert training.get("name") == "[テスト]研修A"
    assert training.get("type") == "Training"
    welfare = [
        a for a in actual if a.get("prize_id") == "test_welfare_prize_id"
    ][0]
    assert welfare.get("name") == "[テスト]休息A"
    assert welfare.get("type") == "Welfare"


def test_fetch_prize(mocker):
    """景品の詳細を取得できること"""

    # give
    test_entry_prize(mocker)
    test_prize_id = "test_training_prize_id"
    response = client.get(
        f"/prize/{test_prize_id}",
    )

    assert response.status_code == 200
    actual_prize = Prize.parse_obj(response.json())
    assert actual_prize.name == "[テスト]研修A"
    assert actual_prize.description == "E2E試験で自動作成されたコンテンツです"
    assert actual_prize.required_token_amount == 2


def test_entry_prize_trade(mocker):
    """景品をトークンと交換できること"""
    # give
    test_entry_prize(mocker)

    test_user_id = "test_user_id"
    test_prize_id = "test_training_prize_id"

    _set_user_balance(mocker, [3, 1])

    response = client.post(
        f"/prize/{test_prize_id}/trade",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual = response.json().get("balance")
    assert actual == 1

    user = users_store.fetch_user(id=test_user_id)
    assert user.purchased_prizes[0].name == "[テスト]研修A"
    assert user.purchased_prizes[0].description == "E2E試験で自動作成されたコンテンツです"

    updated_prize = prizes_store.fetch_prize(id=test_prize_id)
    assert updated_prize.purchased_users[0] == test_user_id


def test_entry_prize_trade_missing(mocker):
    """残高が十分でない場合、景品をトークンと交換できないこと"""
    # give
    test_entry_prize(mocker)

    test_user_id = "test_user_id"
    test_prize_id = "test_training_prize_id"

    _set_user_balance(mocker, [1])

    response = client.post(
        f"/prize/{test_prize_id}/trade",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 400


def _set_user_balance(mocker, balances):
    """テスト用に、指定したユーザの残高を変更する"""
    mocker.patch(  # test_signup_not_existsではトークン量を0で登録し、実際のトークン量=10で更新されることを確認する
        "app.services.prize.entry_prize_trade_service.inosapo_ft.balance_of_address",
        side_effect=balances,
    )

    mocker.patch(  # test_signup_not_existsではトークン量を0で登録し、実際のトークン量=10で更新されることを確認する
        "app.services.prize.entry_prize_trade_service.inosapo_ft.burn",
    )
