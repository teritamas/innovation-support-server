import pytest
from fastapi.testclient import TestClient

from app.facades.nlp import cotoha
from app.main import app
from app.schemas.extension.responses import VerifyVoteEnrichmentResponse

client = TestClient(app)


def test_calculation_judgement_reason_no_high_level_analytics(mocker):
    """AIによるスコアリングを行わない場合、スコアが取得できること"""
    # give
    test_user_id = "test_user_id"
    mocker.patch(
        "app.services.extension.calculation_judgement_reason_service._cotoha_is_active",
        return_value=False,
    )

    response = client.post(
        "/extension/vote/enrichment",
        headers={"Authorization": test_user_id},
        json={
            "judgement_reason": "この提案は私はとてもすらばらしいと思いました。その理由は導入のしやすさが考慮されている点です。実際の医療現場での課題を扱っており、バックエンドもフロントエンドもAPIも活用していて、使えば使うほどデータがたまっていく将来性、この3つの観点で選ばせていただきました。",
        },
    )

    assert response.status_code == 200
    actual = VerifyVoteEnrichmentResponse.parse_obj(response.json())
    assert actual.high_level_analytics == False
    assert actual.rule_score == 0.8


@pytest.mark.skipif(True, reason="CotohaAPIのリクエスト上限を超えないようにするため")
def test_calculation_judgement_reason_use_high_level_analytics(mocker):
    """AIによるスコアリングを行う場合、スコアが取得できること"""
    # give
    test_user_id = "test_user_id"

    # when
    response = client.post(
        "/extension/vote/enrichment",
        headers={"Authorization": test_user_id},
        json={
            "judgement_reason": "この提案は私はとてもすらばらしいと思いました。その理由は導入のしやすさが考慮されている点です。実際の医療現場での課題を扱っており、バックエンドもフロントエンドもAPIも活用していて、使えば使うほどデータがたまっていく将来性、この3つの観点で選ばせていただきました。",
        },
    )

    assert response.status_code == 200
    actual = VerifyVoteEnrichmentResponse.parse_obj(response.json())
    assert actual.high_level_analytics == True
    assert actual.rule_score == 0.8
    assert actual.objective_weight == 0.8
