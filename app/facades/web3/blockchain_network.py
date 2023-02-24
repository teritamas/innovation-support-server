import json
from web3 import Web3

from app.facades.web3.account import ContractOwner


class SmartContract:
    """スマートコントラクトのクラス。ネットワークやアカウントを意識しないで利用可能。"""

    def __init__(
        self,
        contract_owner: ContractOwner,
        contract_address: str,
        api_json_path: str,
        provider_network_url: str = "https://evm.shibuya.astar.network",
    ) -> None:
        self.contract_owner = contract_owner
        self.network = Web3(Web3.HTTPProvider(provider_network_url))
        if self.network.isConnected():
            print(f"Connect Complete !!. network: {provider_network_url}")

        self.contract = self.network.eth.contract(
            address=contract_address, abi=self._load_abi(api_json_path)
        )

        token_name = self.contract.functions.name().call()
        token_symbol = self.contract.functions.symbol().call()
        balance = self.contract.functions.balanceOf(
            Web3.toChecksumAddress(self.contract_owner.address)
        ).call()
        print(
            f"NFT Name: {token_name}, NFT Symbol: {token_symbol}, NFT 残高: {balance}"  # NOQA
        )
        print(
            f"Owner Wallet Address: {contract_owner.address}, 残高: {self.network.eth.get_balance(contract_owner.address)}"  # NOQA
        )

    @staticmethod
    def _load_abi(api_json_path: str):
        with open(api_json_path, "r") as j:
            return json.load(j)

    def execute(self, tx):
        signed_tx = self.network.eth.account.signTransaction(
            tx, self.contract_owner.private_key
        )
        # トランザクションの送信
        tx_hash = self.network.eth.sendRawTransaction(signed_tx.rawTransaction)

        return self.network.eth.waitForTransactionReceipt(tx_hash)


class OZOnlyOwnerMint(SmartContract):
    def __init__(
        self,
        contract_owner: ContractOwner,
        contract_address: str,
        provider_network_url: str = "https://evm.shibuya.astar.network",
    ) -> None:
        super().__init__(
            contract_owner,
            contract_address,
            f"./app/assets/abi/{contract_address}.json",
            provider_network_url,
        )

    def owner(
        self,
    ):
        tx = self.contract.functions.owner().buildTransaction(
            {
                "nonce": self.network.eth.getTransactionCount(
                    self.contract_owner.address
                )
            }
        )
        print(self.execute(tx))

    def name(
        self,
    ):
        tx = self.contract.functions.name().buildTransaction(
            {
                "nonce": self.network.eth.getTransactionCount(
                    self.contract_owner.address
                )
            }
        )
        print(self.execute(tx))
