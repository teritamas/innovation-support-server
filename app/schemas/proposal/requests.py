from typing import List
from pydantic import BaseModel, Field, PositiveInt


class EntryProposalRequest(BaseModel):
    title: str = Field(..., max_length=256, description="idea title")
    descriptions: str = Field(
        ..., max_length=8192, description="idea description."
    )
    attachment_url: str = Field(
        ..., max_length=8192, description="提案を詳細に説明するファイル"
    )
    target_amount: PositiveInt = Field(0, description="")
    is_recruiting_teammates: bool = Field(
        False, description="チームメイトを募集する場合：true　"
    )
    other_contents: str = Field(False, max_length=8192, description="捕捉情報")
    tags: List[str] = Field([], description="キーワード")
    proposer_wallet_address: str = Field(..., description="")
