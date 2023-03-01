from fastapi.testclient import TestClient

from app.facades.database import timelines_store
from app.main import app

client = TestClient(app)


def test_fetch_timeline():
    """タイムラインの一覧取得ができること"""
    # give
    test_user_id = "test_user_id"
    response = client.get(
        "/timeline",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
