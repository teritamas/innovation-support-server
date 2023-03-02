from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_calculation_judgement_reason():
    """投票内容のスコアを算出できること"""
    # give
    test_user_id = "test_user_id"

    response = client.post(
        "/extension/vote/enrichment",
        headers={"Authorization": test_user_id},
        json={
            "judgement_reason": "test_reason",
        },
    )

    assert response.status_code == 200
    assert response.json().get("score") == 0
