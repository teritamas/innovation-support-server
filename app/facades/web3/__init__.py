from app import config
from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.inosapo_ft import InosapoFT
from app.facades.web3.smart_contracts.proposal_nft import ProposalNFT

# 提案用NFT
proposal_nft = ProposalNFT(
    contract_owner=ContractOwner(config.system_wallet_private_key_path),
    provider_network_url=config.provider_network,
    contract_address=config.proposal_nft_contract_address,
)

# 提案用NFT
inosapo_ft = InosapoFT(
    contract_owner=ContractOwner(config.system_wallet_private_key_path),
    provider_network_url=config.provider_network,
    contract_address=config.inosapo_ft_contract_address,
)
