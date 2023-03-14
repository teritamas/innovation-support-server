import asyncio
from re import T

import pytest

from app import config
from app.facades.web3 import inosapo_ft
from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.inosapo_ft import InosapoFT

pytest_plugins = ("pytest_asyncio",)

PROVIDER_NETWORK = config.provider_network
INOSAPO_FT_CONTRACT_ADDRESS = config.inosapo_ft_contract_address
VOTER_ADDRESS = "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"

TEST_SKIP = True


def test_inosapo_ft_contract_function():
    """ネットワークに接続しトランザクションを必要としない関数を実行できること"""
    # 動作確認用なので固定
    inosapo_ft = InosapoFT(
        contract_owner=ContractOwner(config.system_wallet_private_key_path),
        provider_network_url=PROVIDER_NETWORK,
        contract_address=INOSAPO_FT_CONTRACT_ADDRESS,
    )
    assert inosapo_ft.name() == "InnovationSupportFT"
    assert inosapo_ft.owner() == "0x35b1C30648C4c486152EF1AD61A7868CF14cF894"
    assert type(inosapo_ft.balance_of_deposit()) == int
    balance = inosapo_ft.balance_of_address(VOTER_ADDRESS)
    assert type(balance) == int


@pytest.mark.skipif(TEST_SKIP, reason="実際にMintを実行するため時間がかかり、かつテストコインを消費するため")
def test_inosapo_ft_mint_deposit():
    """所有者が発行済みのトークを投票者に分配できること"""
    # 動作確認用なので固定
    inosapo_ft = InosapoFT(
        contract_owner=ContractOwner(config.system_wallet_private_key_path),
        provider_network_url=PROVIDER_NETWORK,
        contract_address=INOSAPO_FT_CONTRACT_ADDRESS,
    )
    assert inosapo_ft.owner() == "0x35b1C30648C4c486152EF1AD61A7868CF14cF894"
    inosapo_ft.mint_deposit()


@pytest.mark.skipif(TEST_SKIP, reason="実際にMintを実行するため時間がかかり、かつテストコインを消費するため")
def test_inosapo_ft_transfer():
    """所有者が発行済みのトークを投票者に分配できること"""
    # 動作確認用なので固定
    inosapo_ft = InosapoFT(
        contract_owner=ContractOwner(config.system_wallet_private_key_path),
        provider_network_url=PROVIDER_NETWORK,
        contract_address=INOSAPO_FT_CONTRACT_ADDRESS,
    )
    assert inosapo_ft.owner() == "0x35b1C30648C4c486152EF1AD61A7868CF14cF894"
    inosapo_ft.transfer(VOTER_ADDRESS, 10)


@pytest.mark.skipif(TEST_SKIP, reason="実際にMintを実行するため時間がかかり、かつテストコインを消費するため")
def test_inosapo_ft_burn():
    """利用者の所持トークンを減らすことができること"""
    # 動作確認用なので固定
    inosapo_ft = InosapoFT(
        contract_owner=ContractOwner(config.system_wallet_private_key_path),
        provider_network_url=PROVIDER_NETWORK,
        contract_address=INOSAPO_FT_CONTRACT_ADDRESS,
    )
    assert inosapo_ft.owner() == "0x35b1C30648C4c486152EF1AD61A7868CF14cF894"
    inosapo_ft.burn(VOTER_ADDRESS, 10)
