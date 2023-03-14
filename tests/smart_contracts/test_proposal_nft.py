import pytest

from app import config
from app.facades.web3 import proposal_nft
from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.proposal_nft import ProposalNFT

pytest_plugins = ("pytest_asyncio",)

PROVIDER_NETWORK = config.provider_network
PROPOSAL_NFT_ADDRESS = config.proposal_nft_contract_address
PROPOSER_ADDRESS = "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"


def test_inosapo_ft_contract_function():
    """ネットワークに接続しトランザクションを必要としない関数を実行できること"""
    # 動作確認用なので固定
    proposal_nft = ProposalNFT(
        contract_owner=ContractOwner(config.system_wallet_private_key_path),
        provider_network_url=PROVIDER_NETWORK,
        contract_address=PROPOSAL_NFT_ADDRESS,
    )
    owner: str = proposal_nft.owner()
    assert owner == "0x35b1C30648C4c486152EF1AD61A7868CF14cF894"


@pytest.mark.skipif(True, reason="実際にMintを実行するため時間がかかり、かつテストコインを消費するため")
@pytest.mark.asyncio
def test_proposal_contract_function():
    """ネットワークに接続しサンプルのコントラクトを実行できること"""
    # 動作確認用なので固定
    test_identifier = "test_abcdefg"
    test_token_amount = 10
    proposal_nft = ProposalNFT(
        contract_owner=ContractOwner(config.system_wallet_private_key_path),
        provider_network_url=PROVIDER_NETWORK,
        contract_address=PROPOSAL_NFT_ADDRESS,
    )
    owner: str = proposal_nft.owner()
    assert owner == "0x35b1C30648C4c486152EF1AD61A7868CF14cF894"

    tokenId = proposal_nft.mint(
        proposer_address=PROPOSER_ADDRESS,  # 決め打ちで自身のMetamask
        identifier=test_identifier,
        amount=test_token_amount,
    )

    assert type(tokenId) == int
    tokenIdentifier = proposal_nft.fetchTokenInfoByTokeId(tokenId=tokenId)
    assert test_identifier == tokenIdentifier
    tokenAmount = proposal_nft.get_token_amount(tokenId=tokenId)
    assert test_token_amount == tokenAmount
