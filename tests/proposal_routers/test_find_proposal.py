from fastapi.testclient import TestClient

from app.facades.database import proposals_store
from app.main import app
from app.schemas.proposal.domain import (
    Proposal,
    ProposalOwnType,
    ProposalStatus,
)
from app.schemas.proposal.dto import ListProposalDto

client = TestClient(app)


def test_find_proposal():
    """提案内容の一覧を取得できること"""

    test_user_id = "test_user_id"
    # give
    response = client.get(
        "/proposal",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual = response.json()
    assert type(actual) == dict
    assert type(actual.get("proposals")) == list


def test_find_proposal_title_query():
    """タイトルで検索して提案内容の一覧を取得できること"""
    test_user_id = "test_user_id"
    proposal_count = 3
    _add_proposal(proposal_count, ProposalStatus.VOTING)
    test_index = 1
    # give
    response = client.get(
        f"/proposal?title=title_{test_index}",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual = response.json()
    assert type(actual) == dict
    actual_proposals = ListProposalDto.parse_obj(
        actual.get("proposals")[0]
    )  # 一つしかない
    assert actual_proposals.title == f"title_{str(test_index)}"
    assert actual_proposals.description == f"description_{str(test_index)}"
    _delete_proposal(proposal_count)


def test_find_proposal_description_query():
    """概要で検索して提案内容の一覧を取得できること"""
    test_user_id = "test_user_id"
    proposal_count = 3
    _add_proposal(proposal_count, ProposalStatus.VOTING)
    test_index = 1
    # give
    response = client.get(
        f"/proposal?description=description_{test_index}",
        headers={"Authorization": test_user_id},
    )
    assert response.status_code == 200
    actual = response.json()
    assert type(actual) == dict
    actual_proposals = ListProposalDto.parse_obj(
        actual.get("proposals")[0]
    )  # 一つしかない
    assert actual_proposals.title == f"title_{str(test_index)}"
    assert actual_proposals.description == f"description_{str(test_index)}"
    _delete_proposal(proposal_count)


def test_find_proposal_status_query():
    """ステータスで検索して提案内容の一覧を取得できること"""
    test_user_id = "test_user_id"
    original_count = _base_count(test_user_id, ProposalStatus.ACCEPT)
    proposal_count = 3

    _add_proposal(proposal_count, ProposalStatus.ACCEPT)
    test_index = 1
    # give
    response = client.get(
        f"/proposal?status=accept",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual = response.json()
    assert type(actual) == dict
    assert len(actual.get("proposals")) == proposal_count + original_count
    _delete_proposal(proposal_count)


def test_find_proposal_tag_query():
    """タグで検索して提案内容の一覧を取得できること"""
    test_user_id = "test_user_id"
    proposal_count = 3
    _add_proposal(proposal_count, ProposalStatus.ACCEPT)
    test_index = 1
    # give
    response = client.get(
        f"/proposal?tag=test",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual = response.json()
    assert type(actual) == dict
    assert len(actual.get("proposals")) == proposal_count
    _delete_proposal(proposal_count)


def test_find_proposal_status_and_title_query():
    """ステータスとタイトル検索して提案内容の一覧を取得できること"""
    test_user_id = "test_user_id"
    proposal_count = 3
    _add_proposal(proposal_count, ProposalStatus.ACCEPT)
    test_index = 1
    # give
    response = client.get(
        f"/proposal?status=accept&title={test_index}",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual = response.json()
    assert type(actual) == dict
    actual_proposals = ListProposalDto.parse_obj(
        actual.get("proposals")[0]
    )  # 一つしかない
    assert actual_proposals.title == f"title_{str(test_index)}"
    assert actual_proposals.description == f"description_{str(test_index)}"

    _delete_proposal(proposal_count)


def test_find_proposal_user_id():
    """user_idを指定して、提案に対するそのユーザのステータスを返すこと"""
    test_user_id = "test_user_id"
    proposal_count = 3
    _add_proposal(proposal_count, ProposalStatus.ACCEPT)

    # give
    response = client.get(
        f"/proposal?user_id={test_user_id}&title=title_",
        headers={"Authorization": test_user_id},
    )

    assert response.status_code == 200
    actual = response.json()
    assert type(actual) == dict

    for d in actual.get("proposals"):
        actual_proposal = ListProposalDto.parse_obj(d)  # 一つしかない
        assert actual_proposal.proposal_own_type == ProposalOwnType.UNVOTED

    _delete_proposal(proposal_count)


def _add_proposal(index, status: ProposalStatus):
    for i in range(index):
        proposal_id = f"proposal_{i}"
        proposals_store.add_proposal(
            proposal_id,
            Proposal(
                title=f"title_{i}",
                description=f"description_{i}",
                proposal_id=proposal_id,
                proposal_status=status,
                tags=[f"tags_{i}", "test"],
            ),
        )


def _delete_proposal(index):
    for i in range(index):
        proposal_id = f"proposal_{i}"
        proposals_store.delete_proposal(proposal_id)


def _base_count(test_user_id: str, status: ProposalStatus):
    base = client.get(
        f"/proposal?status={status}",
        headers={"Authorization": test_user_id},
    ).json()
    return len(base.get("proposals"))
