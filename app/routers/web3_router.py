from fastapi import APIRouter

from app import config
from app.schemas.web3.domain import Contract, ContractType
from app.schemas.web3.response import FindWeb3InfoResponse
from app.utils.authorization import authenticate_key

web3_router = APIRouter(prefix="", tags=["web3"])


@web3_router.get(
    "/web3",
    description="コントラクトの詳細情報取得.",
    response_model=FindWeb3InfoResponse,
)
def find_web3_info():
    return FindWeb3InfoResponse(
        network=config.provider_network,
        contracts=[
            Contract(
                type=ContractType.ERC20,
                address=config.inosapo_ft_contract_address,
                symbol="ISFT",
                decimals=0.1,
                image=None,
            ),
            Contract(
                type=ContractType.ERC721,
                address=config.proposal_nft_contract_address,
                symbol="ISPNFT",
                decimals=0,
                image=None,
            ),
            Contract(
                type=ContractType.OTHERS,
                address=config.proposal_vote_contract_address,
                symbol="",
                decimals=0,
                image=None,
            ),
        ],
    )
