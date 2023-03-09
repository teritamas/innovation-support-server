import json
from typing import List

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.proposal.domain import ProposalPhase


class EntryProposalRequest(BaseModel):
    title: str = Field(..., max_length=256, description="idea title")
    description: str = Field(
        ..., max_length=8192, description="idea description."
    )
    target_amount: PositiveInt = Field(1000, description="目標金額")
    is_recruiting_teammates: bool = Field(
        False, description="チームメイトを募集する場合：true　"
    )
    other_contents: str = Field("その他コメント", max_length=8192, description="補足情報")
    tags: List[str] = Field([], description="キーワード")

    proposal_phase: ProposalPhase = Field(
        ProposalPhase.SEED, description="資金調達の種類"
    )

    slack_notification_channels: List[str] | None = Field(
        None, description="提案の投稿を通知するチャンネル"
    )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
