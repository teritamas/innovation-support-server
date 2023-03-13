import enum
from typing import List

from pydantic import BaseModel, Field

from app.schemas.web3.domain import Contract


class FindWeb3InfoResponse(BaseModel):
    network: str = Field("", description="利用しているコントラクトがデプロイされているネットワーク")

    contracts: List[Contract] = Field([], description="コントラクトの一覧")
