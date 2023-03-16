from fastapi.testclient import TestClient

from app.facades.database import users_store
from app.main import app
from app.schemas.user.domain import AccountType, User

client = TestClient(app)


def test_signup_not_exists(mocker):
    """ユーザが登録済みでない場合、STANDARDユーザで新規登録ができること"""
    # give
    test_user_id = "test_user_id"
    test_wallet_address = "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"
    mocker.patch(
        "app.services.user.entry_user_service.generate_id_str",
        return_value=test_user_id,
    )
    users_store.delete_user(test_user_id)  # 削除してから実行する

    response = client.post(
        "/signup",
        json={
            "user_name": "test_user",
            "wallet_address": test_wallet_address,
        },
    )

    assert response.status_code == 200
    actual_user_id = response.json().get("user_id")
    assert actual_user_id == test_user_id
    assert response.json().get("account_type") == "standard"

    actual_user = users_store.fetch_user(id=actual_user_id)
    assert actual_user.account_type == AccountType.STANDARD
    assert actual_user.wallet_address == test_wallet_address
    assert actual_user.user_name == "test_user"


def test_signup_not_exists_temp_user(mocker):
    """ユーザが登録済みでない場合、Tempユーザで新規登録ができること"""
    # give
    test_user_id = "test_user_id"
    test_mail_address = "test@test.co.jp"
    mocker.patch(
        "app.services.user.entry_user_service.generate_id_str",
        return_value=test_user_id,
    )
    # users_store.delete_user(test_user_id)  # 削除してから実行する

    response = client.post(
        "/signup",
        json={
            "user_name": "test_user",
            "mail_address": test_mail_address,
        },
    )

    assert response.status_code == 200
    actual_user_id = response.json().get("user_id")
    assert actual_user_id == test_user_id
    assert response.json().get("account_type") == "temp"

    actual_user = users_store.fetch_user(id=actual_user_id)
    assert actual_user.account_type == AccountType.TEMP
    assert actual_user.mail_address == test_mail_address
    assert actual_user.user_name == "test_user"


def test_signup_exists(mocker):
    """ユーザが登録済みの場合、そのユーザのIDを返すこと"""
    test_signup_not_exists(mocker=mocker)
    # give
    test_user_id = "test_user_id"
    test_wallet_address = "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"
    mocker.patch(
        "app.services.user.entry_user_service.generate_id_str",
        return_value=test_user_id,
    )

    response = client.post(
        "/signup",
        json={
            "user_name": "test_user",
            "wallet_address": test_wallet_address,
        },
    )

    assert response.status_code == 200
    actual_user_id = response.json().get("user_id")
    assert actual_user_id == test_user_id
    assert response.json().get("account_type") == "standard"

    actual_user = users_store.fetch_user(id=actual_user_id)
    assert actual_user.account_type == AccountType.STANDARD
    assert actual_user.wallet_address == test_wallet_address
    assert actual_user.user_name == "test_user"


def test_login_wallet_address(mocker):
    """ウォレットアドレスを利用してログインができること"""
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


def test_login_mail_address(mocker):
    """メールアドレスを利用してログインができること"""
    test_signup_not_exists_temp_user(mocker)
    # give
    test_user_id = "test_user_id"
    test_mail_address = "test@test.co.jp"

    response = client.get(
        f"/login/mail_address/{test_mail_address}",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual_user = User.parse_obj(response.json())
    assert actual_user.user_id == test_user_id
    assert actual_user.total_token_amount == 0
    assert actual_user.user_name == "test_user"
    assert actual_user.message == ""
    assert actual_user.mail_address == test_mail_address
