from web3 import Web3, EthereumTesterProvider
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from eth_account import Account
import secrets

from app.services.web3.account import ContractOwner
from app.services.web3.blockchain_network import OZOnlyOwnerMint, SmartContract

client = ContractOwner("./key/dev_private.key")
sample = OZOnlyOwnerMint(
    contract_owner=client,
    provider_network_url="https://evm.shibuya.astar.network",
    contract_address="0xbAb5B35CA552BffC32445e2336C38759dbB6E3Cc",
    api_json_path="./contract.json",
)

sample.owner()
