from fastapi.testclient import TestClient

from app.main import app
from app.schemas.user.domain import User

client = TestClient(app)


def test_entry_user(mocker):
    # give
    test_user_id = "test_uuid"
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
    test_entry_user(mocker)
    # give
    test_user_id = "test_uuid"

    response = client.get(
        f"/user/{test_user_id}",
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
    # test_entry_user(mocker)
    # give
    test_user_id = "test_uuid"
    test_wallet_address = "0x7FF84a54d3d7070391Dd9808696Fc547a910af91"

    response = client.get(
        f"/user/wallet_address/{test_wallet_address}",
    )

    assert response.status_code == 200
    actual_user = User.parse_obj(response.json())
    assert actual_user.user_id == test_user_id
    assert actual_user.total_token_amount == 0
    assert actual_user.user_name == "test_user"
    assert actual_user.message == ""
    assert actual_user.wallet_address == test_wallet_address
