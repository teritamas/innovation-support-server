from fastapi.testclient import TestClient

from app.facades.database import users_store
from app.main import app
from app.schemas.user.domain import User

client = TestClient(app)


def test_signup_not_exists(mocker):
    """ユーザが登録済みでない場合、新規登録ができること"""
    # give
    test_user_id = "test_user_id"
    mocker.patch(
        "app.services.user.entry_user_service.generate_id_str",
        return_value=test_user_id,
    )
    users_store.delete_user(test_user_id)  # 削除してから実行する

    response = client.post(
        "/signup",
        json={
            "user_name": "test_user",
            "wallet_address": "0xb872960EF2cBDecFdC64115E1C77067c16f042FB",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"user_id": f"{test_user_id}"}


def test_signup_exists(mocker):
    """ユーザが登録済みの場合、そのユーザのIDを返すこと"""
    test_signup_not_exists(mocker=mocker)
    # give
    test_user_id = "test_user_id"
    mocker.patch(
        "app.services.user.entry_user_service.generate_id_str",
        return_value=test_user_id,
    )

    response = client.post(
        "/signup",
        json={
            "user_name": "test_user",
            "wallet_address": "0xb872960EF2cBDecFdC64115E1C77067c16f042FB",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"user_id": f"{test_user_id}"}


def test_login_wallet_address(mocker):
    # test_signup_not_exists(mocker)
    # give
    test_user_id = "test_user_id"
    test_wallet_address = "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"

    response = client.get(
        f"/login/wallet_address/{test_wallet_address}",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual_user = User.parse_obj(response.json())
    assert actual_user.user_id == test_user_id
    assert actual_user.total_token_amount == 0
    assert actual_user.user_name == "test_user"
    assert actual_user.message == ""
    assert actual_user.wallet_address == test_wallet_address
