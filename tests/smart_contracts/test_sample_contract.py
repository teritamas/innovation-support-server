import pytest

from app import config
from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.sample_contract import SampleNFT

pytest_plugins = ("pytest_asyncio",)

PROVIDER_NETWORK = "https://goerli.blockpi.network/v1/rpc/public"
SAMPLE_CONTRACT_ADDRESS = "0x99802244430b37362Eb494ec5Ce92fBC8F38f36C"


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
