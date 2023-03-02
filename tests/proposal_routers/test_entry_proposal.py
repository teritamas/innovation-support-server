import json

import pytest
from fastapi.testclient import TestClient

from app.facades.database import proposals_store
from app.facades.storage import proposal_pdf
from app.main import app
from app.schemas.proposal.responses import EntryProposalResponse
from app.utils.common import build_nft_uri
from tests.test_account_router import test_signup_not_exists

client = TestClient(app)


def test_entry_proposal(mocker):
    """提案を追加する"""
    test_signup_not_exists(mocker=mocker)
    test_proposal_id = "test_proposal_id"
    test_user_id = "test_user_id"
    test_file_name = "sample.pdf"
    test_token_id = 1
    mocker.patch(
        "app.services.proposal.entry_proposal_service.generate_id_str",
        return_value=test_proposal_id,
    )
    mocker.patch(
        "app.services.proposal.entry_proposal_service.proposal_nft.mint",
        return_value=test_token_id,
    )
    proposals_store.delete_proposal(test_proposal_id)
    proposal_pdf.delete(
        build_nft_uri(
            user_id=test_user_id,
            proposal_id=test_proposal_id,
            filename=test_file_name,
        )
    )

    request = {
        "title": "pytestの実行サンプル",
        "description": "テストで挿入されたデータです",
        "target_amount": 1000,
        "is_recruiting_teammates": False,
        "other_contents": "その他コメント",
        "tags": [],
    }
    request_json = json.dumps(request)
    response = client.post(
        "/proposal",
        headers={"Authorization": test_user_id},
        files={
            "request": (
                None,
                request_json,
            ),
            "file": open(f"./tests/assets/{test_file_name}", "rb"),
        },
    )
    assert response.status_code == 200
    actual = EntryProposalResponse.parse_obj(response.json())
    assert actual.proposal_id == test_proposal_id


@pytest.mark.skipif(True, reason="実際にSlackに通知が飛ぶため、基本的にスキップ")
def test_entry_proposal_slack_notification(mocker):
    """提案を追加し、Slackに通知が行われること"""
    test_user_id = "test_user_id"
    test_proposal_id = "test_proposal_id"
    test_file_name = "sample.pdf"
    mocker.patch(
        "app.services.proposal.entry_proposal_service.generate_id_str",
        return_value=test_proposal_id,
    )
    proposals_store.delete_proposal(test_proposal_id)
    proposal_pdf.delete(
        build_nft_uri(
            user_id=test_user_id,
            proposal_id=test_proposal_id,
            filename=test_file_name,
        )
    )
    request = {
        "title": "pytestの実行サンプル",
        "description": "テストで挿入されたデータです",
        "target_amount": 1000,
        "is_recruiting_teammates": False,
        "other_contents": "その他コメント",
        "tags": [],
        "slack_notification_channels": ["general", "for_develop"],
    }
    request_json = json.dumps(request)
    response = client.post(
        "/proposal",
        headers={"Authorization": test_user_id},
        files={
            "request": (
                None,
                request_json,
            ),
            "file": open(f"./tests/assets/{test_file_name}", "rb"),
        },
    )
    assert response.status_code == 200
    actual = EntryProposalResponse.parse_obj(response.json())
    assert actual.proposal_id == test_proposal_id
