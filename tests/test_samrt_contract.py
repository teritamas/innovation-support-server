import asyncio

import pytest

from app import config
from app.facades.web3 import proposal_nft
from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.proposal_nft import ProposalNFT
from app.facades.web3.smart_contracts.sample_contract import SampleNFT

pytest_plugins = ("pytest_asyncio",)

PROVIDER_NETWORK = "https://goerli.blockpi.network/v1/rpc/public"
SAMPLE_CONTRACT_ADDRESS = "0x99802244430b37362Eb494ec5Ce92fBC8F38f36C"
PERSONAL_NFT_ADDRESS = "0x46f14F3Dd30465Fa2AA1cA929BceFc9FeE2ad0c9"
PROPOSER_ADDRESS = "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"


def test_proposal_nft_mock_function():
    """提案NFTのMockの関数が実行できること"""

    proposal_nft.vote("test_nft_address", "test_voter_address", 10)
    proposal_nft.burn("test_address", 10)


@pytest.mark.skipif(True, reason="実際にMintを実行するため時間がかかり、かつテストコインを消費するため")
def test_sample_contract_function():
    """ネットワークに接続しサンプルのコントラクトを実行できること"""
    # 動作確認用なので固定
    sample = SampleNFT(
        contract_owner=ContractOwner(config.system_wallet_private_key_path),
        provider_network_url=PROVIDER_NETWORK,
        contract_address=SAMPLE_CONTRACT_ADDRESS,
    )

    assert sample.name() != ""
    assert sample.owner() != ""


@pytest.mark.skipif(True, reason="実際にMintを実行するため時間がかかり、かつテストコインを消費するため")
@pytest.mark.asyncio
async def test_proposal_contract_function():
    """ネットワークに接続しサンプルのコントラクトを実行できること"""
    # 動作確認用なので固定
    test_identifier = "abcdefg"
    proposal_nft = ProposalNFT(
        contract_owner=ContractOwner(config.system_wallet_private_key_path),
        provider_network_url=PROVIDER_NETWORK,
        contract_address=PERSONAL_NFT_ADDRESS,
    )
    owner: str = proposal_nft.owner()

    tokenId = await proposal_nft.mint(
        proposer_address=PROPOSER_ADDRESS,  # 決め打ちで自身のMetamask
        identifier=test_identifier,
    )

    assert type(tokenId) == int
    tokenIdentifier = proposal_nft.fetchTokenInfoByTokeId(tokenId=tokenId)
    assert test_identifier == tokenIdentifier
