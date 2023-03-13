from typing import List

from pydantic import BaseModel, Field


class VerifyVoteEnrichmentDto(BaseModel):
    rule_score: float = Field(0, description="ルールベースによって判定されたスコア.")
    high_level_analytics: bool = Field(
        False, description="AIを利用した高度な解析を含めている場合,True"
    )
    sentence_is_positive: bool = Field(
        False, description="文章がポジティブな文章の場合,True."
    )
    sentence_keywords: List[str] = Field([], description="文章に含まれるキーワードのリスト")
    emotional_keywords: List[str] = Field([], description="文章に含まれる感情的な発言のリスト")
    objective_weight: float = Field(0, description="文章の客観度合い.")
    objective_score: float = Field(
        0, description="文章の客観度合い x rule_scoreで算出される."
    )

    expected_reword_token_amount: int = Field(0, description="この文章で期待できるトークン量")
