from datetime import datetime

from pydantic import BaseModel, Field

from app.utils.common import now


class ProposalVote(BaseModel):
    """提案に対する投票"""

    # proposal_id: str = Field("", description="ユーザID")
    user_id: str = Field("", description="投票者のユーザID")
    judgement: bool = Field(False, description="投票結果")
    judgement_reason: str = Field("", description="投票理由")
    mint_token_amount: int = Field(0, description="投票でユーザに発行されたトークン量")

    created_at: datetime = Field(now(), description="作成時刻")
    updated_at: datetime = Field(now(), description="編集時刻")

    # コントラクトに関する設定
    # nft_uri: str = Field("", description="投票NFTのURI")
    # nft_token_id: str = Field("", description="投票NFTのトークンID")


class ProposalVoteOnContract(BaseModel):
    address: str = Field("", description="提案者のウォレットアドレス")
    vote_total_count: int = Field(0, description="投票総数")
    vote_agreement_count: int = Field(0, description="賛成の票数")
    voting_status: int = Field(0, description="0: 投票中, 1: 承認, 2:拒否")
