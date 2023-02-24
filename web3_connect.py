from app.services.web3.account import ContractOwner
from app.services.web3.blockchain_network import OZOnlyOwnerMint

client = ContractOwner("./key/dev_private.key")
sample = OZOnlyOwnerMint(
    contract_owner=client,
    # provider_network_url="https://evm.shibuya.astar.network",
    provider_network_url="https://goerli.blockpi.network/v1/rpc/public",
    contract_address="0x99802244430b37362Eb494ec5Ce92fBC8F38f36C",
    api_json_path="./contract.json",
)

# sample.owner()
sample.name()
