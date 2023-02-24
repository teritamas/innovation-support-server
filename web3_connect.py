from app.facades.web3.account import ContractOwner
from app.facades.web3.blockchain_network import OZOnlyOwnerMint

# サンプル用のコントラクト
SAMPLE_CONTRACT_ADDRESS = "0x99802244430b37362Eb494ec5Ce92fBC8F38f36C"

client = ContractOwner("./key/dev_private.key")

sample = OZOnlyOwnerMint(
    contract_owner=client,
    # provider_network_url="https://evm.shibuya.astar.network",
    provider_network_url="https://goerli.blockpi.network/v1/rpc/public",
    contract_address=SAMPLE_CONTRACT_ADDRESS,
)

# sample.owner()
sample.name()
