from datetime import timedelta

import pytest

from app.facades.database import proposals_store
from app.schemas.proposal.domain import JudgementStatusDto, ProposalStatus
from app.services.proposal import judgement_proposal_service
from app.utils.common import now
from scripts import sample_vote
from tests.proposal_routers.test_entry_proposal import test_entry_proposal

VOTER_COUNT = 50
TEST_SKIP = True  # 試験を実行する場合、Falseにする
TEST_SKIP_CONTRACT = True  # スマートコントラクトの実行をする試験


@pytest.mark.skipif(TEST_SKIP, reason="ダミーユーザを挿入する処理でFireStoreの書き込みが急増するため")
@pytest.mark.asyncio
def test_entry_judgement_proposal_accept(mocker):
    """条件を満たしている提案のステータスが承認状態であること"""
    # give
    test_proposal_id = "test_proposal_id"
    test_entry_proposal(mocker)  # ダミーの提案を登録
    # Seedの投票期間である7 + 1日前の日付を返すようにする。
    _update_date(proposal_id=test_proposal_id, date=7)

    agreement_rate: float = 0.5
    sample_vote.main(
        test_proposal_id,
        voter_count=VOTER_COUNT,
        agreement_rate=agreement_rate,
        is_complete_vote=False,  # 自動で１年前の日付にする処理を外す
    )

    mocker.patch(
        "app.services.proposal.entry_proposal_service.proposal_vote.judgement_proposal",
    )
    # when
    actual: JudgementStatusDto = judgement_proposal_service.execute(
        proposal_id=test_proposal_id
    )

    # then
    assert ProposalStatus.ACCEPT == actual.proposal_status
    assert True == actual.is_limit
    assert True == actual.fill_min_agreement_count
    assert True == actual.fill_min_voter_count

    proposal = proposals_store.fetch_proposal(test_proposal_id)
    assert ProposalStatus.ACCEPT == proposal.proposal_status


@pytest.mark.skipif(TEST_SKIP, reason="ダミーユーザを挿入する処理でFireStoreの書き込みが急増するため")
def test_entry_judgement_proposal_reject(mocker):
    """条件を満たしていない提案のステータスが棄却状態であること"""
    # give
    test_proposal_id = "test_proposal_id"
    test_entry_proposal(mocker)  # ダミーの提案を登録
    # Seedの投票期間である7 + 1日前の日付を返すようにする。
    _update_date(proposal_id=test_proposal_id, date=7)
    agreement_rate: float = 0.49  # Middleの棄却要件
    sample_vote.main(
        test_proposal_id,
        voter_count=VOTER_COUNT,
        agreement_rate=agreement_rate,
        is_complete_vote=False,  # 自動で１年前の日付にする処理を外す
    )
    mocker.patch(
        "app.services.proposal.entry_proposal_service.proposal_vote.judgement_proposal",
    )
    # when
    actual: JudgementStatusDto = judgement_proposal_service.execute(
        proposal_id=test_proposal_id
    )

    # then
    assert ProposalStatus.REJECT == actual.proposal_status
    assert True == actual.is_limit
    assert False == actual.fill_min_agreement_count
    assert True == actual.fill_min_voter_count

    proposal = proposals_store.fetch_proposal(test_proposal_id)
    assert ProposalStatus.REJECT == proposal.proposal_status


def test_entry_judgement_proposal_voting(mocker):
    """日付条件を満たしていない提案のステータスが投票状態であること"""
    # give
    test_proposal_id = "test_proposal_id"

    test_entry_proposal(mocker)  # ダミーの提案を登録
    # Seedの投票期間である7 + 1日前の日付を返すようにする。
    _update_date(proposal_id=test_proposal_id, date=6)

    agreement_rate: float = 0.59  # Middleの棄却要件
    sample_vote.main(
        test_proposal_id,
        voter_count=10,
        agreement_rate=agreement_rate,
        is_complete_vote=False,  # 自動で１年前の日付にする処理を外す
    )
    # when
    actual: JudgementStatusDto = judgement_proposal_service.execute(
        proposal_id=test_proposal_id
    )

    # then
    assert ProposalStatus.VOTING == actual.proposal_status
    assert False == actual.is_limit
    assert False == actual.fill_min_agreement_count
    assert False == actual.fill_min_voter_count

    proposal = proposals_store.fetch_proposal(test_proposal_id)
    assert ProposalStatus.VOTING == proposal.proposal_status


@pytest.mark.skipif(TEST_SKIP_CONTRACT, reason="コントラクトを実行する処理のため")
def test_entry_judgement_proposal_accept_run_contract(mocker):
    """条件を満たしている提案のステータスが承認でき、コントラクトも正常に実行可能であること"""
    # give
    test_proposal_id = "test_proposal_id"

    test_entry_proposal(mocker)  # ダミーの提案を登録
    # Seedの投票期間である7 + 1日前の日付を返すようにする。
    _update_date(proposal_id=test_proposal_id, date=7)

    agreement_rate: float = 0.6
    sample_vote.main(
        test_proposal_id,
        voter_count=VOTER_COUNT,
        agreement_rate=agreement_rate,
        is_complete_vote=False,  # 自動で１年前の日付にする処理を外す
    )

    # when
    actual: JudgementStatusDto = judgement_proposal_service.execute(
        proposal_id=test_proposal_id
    )

    # then
    assert ProposalStatus.ACCEPT == actual.proposal_status
    assert True == actual.is_limit
    assert True == actual.fill_min_agreement_count
    assert True == actual.fill_min_voter_count

    proposal = proposals_store.fetch_proposal(test_proposal_id)
    assert ProposalStatus.ACCEPT == proposal.proposal_status


def _update_date(proposal_id, date):
    """テスト用に登録した提案の日付を変更する"""
    proposal = proposals_store.fetch_proposal(proposal_id)
    # 作成日を１年前にすることで、すべての投票期間を必ず超えるので、投票が終了する。
    proposal.created_at = now() - timedelta(days=date)

    proposals_store.add_proposal(id=proposal_id, content=proposal)
