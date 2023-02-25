import pytest

from app import config
from app.facades.web3 import proposal_nft
from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts import SampleNFT


def test_proposal_nft_contract_function():
    """提案NFTの各機能が実行できること"""

    proposal_nft.mint("test_proposer_address", "test_bucket_path")
    proposal_nft.vote("test_nft_address", "test_voter_address", 10)
    proposal_nft.burn("test_address", 10)


@pytest.mark.skipif(True, reason="実際にMintを実行するため時間がかかり、かつテストコインを消費するため")
def test_sample_contract_function():
    """ネットワークに接続しサンプルのコントラクトを実行できること"""
    # 動作確認用なので固定
    SAMPLE_CONTRACT_ADDRESS = "0x99802244430b37362Eb494ec5Ce92fBC8F38f36C"
    PROVIDER_NETWORK = "https://goerli.blockpi.network/v1/rpc/public"
    sample = SampleNFT(
        contract_owner=ContractOwner(config.system_wallet_private_key_path),
        provider_network_url=PROVIDER_NETWORK,
        contract_address=SAMPLE_CONTRACT_ADDRESS,
    )

    sample.owner()
    sample.name()
