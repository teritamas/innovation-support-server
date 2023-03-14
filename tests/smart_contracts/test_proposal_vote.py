import pytest

from app import config
from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.proposal_vote import ProposalVoteContract
from app.schemas.proposal_vote.domain import ProposalVoteOnContract

pytest_plugins = ("pytest_asyncio",)

PROVIDER_NETWORK = config.provider_network
PROPOSAL_NFT_ADDRESS = config.proposal_nft_contract_address
VOTER_ADDRESS = "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"
TEST_NFT_ID = 1  # テスト用でほぼ必ず存在してるため

# 提案用NFT
proposal_vote = ProposalVoteContract(
    contract_owner=ContractOwner(config.system_wallet_private_key_path),
    provider_network_url=config.provider_network,
    proposal_nft_contract_address=config.proposal_nft_contract_address,
    inosapo_ft_contract_address=config.inosapo_ft_contract_address,
    contract_address=config.proposal_vote_contract_address,
)


@pytest.mark.skipif(True, reason="実際にMintを実行するため時間がかかり、かつテストコインを消費するため")
@pytest.mark.asyncio
async def test_proposal_vote_entry():
    """提案内容の投票を開始できること"""
    proposal_vote.entry_proposal(TEST_NFT_ID)


@pytest.mark.skipif(True, reason="実際にMintを実行するため時間がかかり、かつテストコインを消費するため")
@pytest.mark.asyncio
async def test_proposal_vote_vote():
    """提案内容に対して投票ができること"""
    proposal_vote.vote(TEST_NFT_ID, VOTER_ADDRESS, True)

    # ２回目は失敗すること
    with pytest.raises(Exception) as e:
        proposal_vote.vote(TEST_NFT_ID, VOTER_ADDRESS, True)


def test_proposal_vote_get_stats():
    """投票状態を取得"""
    status: ProposalVoteOnContract = proposal_vote.get_status(1)

    assert status.address == VOTER_ADDRESS
    assert status.vote_total_count >= 1
    assert status.vote_agreement_count >= 1
