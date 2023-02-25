from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts import ProposalNFT

# サンプル用のコントラクト
SAMPLE_CONTRACT_ADDRESS = "0x99802244430b37362Eb494ec5Ce92fBC8F38f36C"

proposal_nft = ProposalNFT(
    contract_owner=ContractOwner("./key/dev_private.key"),
    # provider_network_url="https://evm.shibuya.astar.network",
    provider_network_url="https://goerli.blockpi.network/v1/rpc/public",
    contract_address=SAMPLE_CONTRACT_ADDRESS,
)
