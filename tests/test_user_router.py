from fastapi.testclient import TestClient

from app.main import app
from app.schemas.user.domain import User
from tests.test_account_router import test_signup_not_exists

client = TestClient(app)


def test_fetch_user(mocker):
    test_signup_not_exists(mocker)
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
