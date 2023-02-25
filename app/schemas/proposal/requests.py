import json
from typing import List

from pydantic import BaseModel, Field, PositiveInt


class EntryProposalRequest(BaseModel):
    title: str = Field(..., max_length=256, description="idea title")
    descriptions: str = Field(
        ..., max_length=8192, description="idea description."
    )
    target_amount: PositiveInt = Field(1000, description="目標金額")
    is_recruiting_teammates: bool = Field(
        False, description="チームメイトを募集する場合：true　"
    )
    other_contents: str = Field("その他コメント", max_length=8192, description="捕捉情報")
    tags: List[str] = Field([], description="キーワード")
    proposer_wallet_address: str = Field(..., description="")

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
