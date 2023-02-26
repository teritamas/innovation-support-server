import json
import os

import pytest
from fastapi.testclient import TestClient

from app.facades.database import proposals_store
from app.facades.storage import proposal_pdf
from app.main import app
from app.schemas.proposal.domain import Proposal
from app.schemas.proposal.responses import EntryProposalResponse
from app.schemas.user.domain import User
from app.utils.common import build_nft_uri
from tests.test_user_router import test_entry_user

client = TestClient(app)


def test_entry_proposal(mocker):
    test_entry_user(mocker=mocker)
    test_proposal_id = "test_proposal_id"
    test_user_id = "test_uuid"
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
        "descriptions": "テストで挿入されたデータです",
        "target_amount": 1000,
        "is_recruiting_teammates": False,
        "other_contents": "その他コメント",
        "tags": [],
        "user_id": test_user_id,
    }
    request_json = json.dumps(request)
    response = client.post(
        "/proposal",
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
    test_proposal_id = "test_proposal_id"
    test_wallet_address = "0x7FF84a54d3d7070391Dd9808696Fc547a910af91"
    test_file_name = "sample.pdf"
    mocker.patch(
        "app.services.proposal.entry_proposal_service.generate_id_str",
        return_value=test_proposal_id,
    )
    proposals_store.delete_proposal(test_proposal_id)
    proposal_pdf.delete(
        os.path.join(test_wallet_address, test_proposal_id, test_file_name)
    )

    request = {
        "title": "pytestの実行サンプル",
        "descriptions": "テストで挿入されたデータです",
        "target_amount": 1000,
        "is_recruiting_teammates": False,
        "other_contents": "その他コメント",
        "tags": [],
        "proposer_wallet_address": test_wallet_address,
        "slack_notification_channels": ["general", "for_develop"],
    }
    request_json = json.dumps(request)
    response = client.post(
        "/proposal",
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


def test_find_proposal():
    # give
    response = client.get(
        "/proposal",
    )

    assert response.status_code == 200
    actual = response.json()
    assert type(actual) == dict
    assert type(actual.get("proposals")) == list


def test_fetch_proposal(mocker):
    test_entry_proposal(mocker)
    # give
    test_proposal_id = "test_proposal_id"
    response = client.get(
        f"/proposal/{test_proposal_id}",
    )

    assert response.status_code == 200
    actual_proposal = Proposal.parse_obj(response.json().get("proposal"))
    assert actual_proposal.proposal_id == test_proposal_id
    actual_user = User.parse_obj(response.json().get("proposal_user"))
    assert actual_user.user_id == "test_uuid"
