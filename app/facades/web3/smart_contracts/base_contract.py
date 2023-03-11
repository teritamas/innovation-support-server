import json

from web3 import Web3

from app.facades.web3.account import ContractOwner
from app.utils.logging import logger


class BaseContract:
    """スマートコントラクトの基底クラス。ネットワークやアカウントを意識しないで利用可能。"""

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
            logger.info(
                f"Connect Complete !!. network: {provider_network_url}"
            )

        self.contract = self.network.eth.contract(
            address=contract_address, abi=self._load_abi(api_json_path)
        )

        token_name = self.contract.functions.name().call()
        token_symbol = self.contract.functions.symbol().call()
        balance = self.contract.functions.balanceOf(
            Web3.toChecksumAddress(self.contract_owner.address)
        ).call()
        logger.info(
            f"NFT Name: {token_name}, NFT Symbol: {token_symbol}, NFT 残高: {balance}"  # NOQA
        )
        logger.info(
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

        return self.network.eth.wait_for_transaction_receipt(tx_hash)

    def owner(
        self,
    ):
        return self.contract.functions.owner().call()

    def name(
        self,
    ):
        return self.contract.functions.name().call()

    def fetchTokenInfoByTokeId(self, tokenId: int):
        return self.contract.functions.tokenURI(tokenId).call()

    def convert_checksum_address(self, address: str) -> str:
        return Web3.toChecksumAddress(address)
