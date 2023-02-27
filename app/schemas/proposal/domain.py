from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.utils.common import now


class Proposal(BaseModel):
    """提案内容ドメイン"""

    proposal_id: str = Field(
        "abcdefg", max_length=256, description="識別する固有のID"
    )
    title: str = Field("タイトルサンプル", max_length=256, description="提案のタイトル")
    descriptions: str = Field(
        "提案の概要サンプル", max_length=8192, description="提案の概要"
    )
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
    created_at: datetime = Field(now(), description="作成時刻")
    updated_at: datetime = Field(now(), description="編集時刻")

    # 提案者に関するユーザID
    user_id: str = Field("", description="提案者のユーザID")

    # コントラクトに関する設定
    nft_uri: str = Field("", description="提案NFTのURI")
    nft_token_id: str = Field("", description="提案NFTのトークンID")
