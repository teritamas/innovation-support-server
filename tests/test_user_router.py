from fastapi.testclient import TestClient

from app.facades.database import users_store
from app.main import app
from app.schemas.user.domain import User

client = TestClient(app)


def test_entry_user_not_exists(mocker):
    """ユーザが登録済みでない場合、新規登録ができること"""
    # give
    test_user_id = "test_user_id"
    mocker.patch(
        "app.services.user.entry_user_service.generate_id_str",
        return_value=test_user_id,
    )
    users_store.delete_user(test_user_id)  # 削除してから実行する

    response = client.post(
        "/user",
        json={
            "user_name": "test_user",
            "wallet_address": "0x7FF84a54d3d7070391Dd9808696Fc547a910af91",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"user_id": f"{test_user_id}"}


def test_entry_user_exists(mocker):
    """ユーザが登録済みの場合、そのユーザのIDを返すこと"""
    test_entry_user_not_exists(mocker=mocker)
    # give
    test_user_id = "test_user_id"
    mocker.patch(
        "app.services.user.entry_user_service.generate_id_str",
        return_value=test_user_id,
    )

    response = client.post(
        "/user",
        json={
            "user_name": "test_user",
            "wallet_address": "0x7FF84a54d3d7070391Dd9808696Fc547a910af91",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"user_id": f"{test_user_id}"}


def test_fetch_user(mocker):
    test_entry_user_not_exists(mocker)
    # give
    test_user_id = "test_user_id"

    response = client.get(
        f"/user/{test_user_id}",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual_user = User.parse_obj(response.json())
    assert actual_user.user_id == test_user_id
    assert actual_user.total_token_amount == 0
    assert actual_user.user_name == "test_user"
    assert actual_user.message == ""
    assert (
        actual_user.wallet_address
        == "0x7FF84a54d3d7070391Dd9808696Fc547a910af91"
    )


def test_fetch_user_by_wallet_address(mocker):
    # test_entry_user_not_exists(mocker)
    # give
    test_user_id = "test_user_id"
    test_wallet_address = "0x7FF84a54d3d7070391Dd9808696Fc547a910af91"

    response = client.get(
        f"/user/wallet_address/{test_wallet_address}",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual_user = User.parse_obj(response.json())
    assert actual_user.user_id == test_user_id
    assert actual_user.total_token_amount == 0
    assert actual_user.user_name == "test_user"
    assert actual_user.message == ""
    assert actual_user.wallet_address == test_wallet_address
