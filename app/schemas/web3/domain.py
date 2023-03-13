from enum import Enum

from pydantic import BaseModel, Field


class ContractType(str, Enum):
    OTHERS = "other"
    ERC20 = "ERC20"
    ERC721 = "ERC721"


class Contract(BaseModel):
    type: ContractType = Field("", description="コントラクトの種類")
    address: str = Field("", description="コントラクトアドレス")
    symbol: str = Field("", description="トークンのシンボル")
    decimals: float = Field(0, description="有効な小数点桁数")
    image: str | None = Field(None, description="(オプション)トークンの画像")
