from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from app.schemas.proposal_vote.domain import ProposalVote
from app.utils.common import now


class ProposalPhase(str, Enum):
    """https://expact.jp/series-a/"""

    SEED = "seed"  # シード期
    EARLY = "early"
    MIDDLE = "middle"
    LATER = "later"
    GROWTH = "growth"


class ProposalStatus(str, Enum):
    VOTING = "voting"  # 投票中
    REJECT = "reject"  # 否決
    ACCEPT = "accept"  # 可決


from pydantic.dataclasses import dataclass


class ProposalFundraisingCondition(BaseModel):
    """資金調達の条件"""

    limit_date: int = Field(0, description="締切までの期間")
    procurement_token_amount: int = Field(10, description="調達可能なトークン量")
    min_voter_count: int = Field(0, description="最低投票数")
    min_agreement_count: float = Field(0, description="賛成の割合(%)")


class Proposal(BaseModel):
    """提案内容ドメイン"""

    proposal_id: str = Field(
        "abcdefg", max_length=256, description="識別する固有のID"
    )
    title: str = Field("タイトルサンプル", max_length=256, description="提案のタイトル")
    description: str = Field("提案の概要サンプル", max_length=8192, description="提案の概要")
    file_original_name: str = Field(
        "proposal.pdf",
        max_length=8192,
        description="アップロードされたファイルの元々のファイル名。",
    )
    target_amount: int = Field(0, description="目標金額(万円)")
    is_recruiting_teammates: bool = Field(
        False, description="チームメイトを募集する場合：true　"
    )
    other_contents: str = Field(False, max_length=8192, description="捕捉情報")
    tags: List[str] = Field(["サンプルA", "サンプルB"], description="キーワード")
    proposal_status: ProposalStatus = Field(
        ProposalStatus.VOTING, description="投票状態"
    )
    proposal_phase: ProposalPhase = Field(
        ProposalPhase.SEED, description="資金調達の種類"
    )

    created_at: datetime = Field(now(), description="作成時刻")
    updated_at: datetime = Field(now(), description="編集時刻")

    # 提案者に関するユーザID
    user_id: str = Field("", description="提案者のユーザID")

    # コントラクトに関する設定
    nft_uri: str = Field("", description="提案NFTのURI")
    nft_token_id: str = Field("", description="提案NFTのトークンID")

    # 投票
    proposal_fundraising_condition: ProposalFundraisingCondition | None = (
        Field(None, description="資金調達の条件")
    )
    votes: List[ProposalVote] = Field([], description="この提案に対して投票された内容")

    # その他
    thumbnail_filename: str = Field("", description="サムネイル画像のファイルパス")
