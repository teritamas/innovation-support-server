from typing import List

from pydantic import BaseModel, Field, PositiveInt


class Proposal(BaseModel):
    """提案内容ドメイン"""

    proposal_id: str = Field(
        "abcdefg", max_length=256, description="idea title"
    )
    title: str = Field("タイトルサンプル", max_length=256, description="idea title")
    descriptions: str = Field(
        "提案の概要サンプル", max_length=8192, description="idea description."
    )
    bucket_path: str = Field(
        "path/to/proposal.pdf",
        max_length=8192,
        description="提案を詳細に説明するファイルのパス",
    )
    target_amount: PositiveInt = Field(1000, description="目標金額")
    is_recruiting_teammates: bool = Field(
        False, description="チームメイトを募集する場合：true　"
    )
    other_contents: str = Field(False, max_length=8192, description="捕捉情報")
    tags: List[str] = Field(["サンプルA", "サンプルB"], description="キーワード")
    user_id: str = Field("提案者のユーザID", description="")

    # コントラクトに関する設定
    nft_token_id: str = Field("提案NFTのID", description="提案NFTのID")
