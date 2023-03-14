from web3 import Web3

from app import config
from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.base_contract import BaseContract
from app.utils.logging import logger


class InosapoFT(BaseContract):
    """トークン発行のコントラクト"""

    def __init__(
        self,
        contract_owner: ContractOwner,
        contract_address: str,
        provider_network_url: str = "https://evm.shibuya.astar.network",
        mock_mode: bool = False,
    ) -> None:
        if mock_mode:  # MockModeの時は初期化しない
            return

        super().__init__(
            contract_owner,
            contract_address,
            f"./app/assets/abi/{contract_address}.json",
            provider_network_url,
        )
        token_name = self.contract.functions.name().call()
        token_symbol = self.contract.functions.symbol().call()
        balance = self.contract.functions.balanceOf(
            Web3.toChecksumAddress(self.contract_owner.address)
        ).call()
        logger.info(
            f"Contract Name: {token_name}, Symbol: {token_symbol}, 残高: {balance}"  # NOQA
        )

    def owner(
        self,
    ):
        """コントラクトの所有者を取得"""
        return self.contract.functions.owner().call()

    def name(
        self,
    ):
        """コントラクトの名称を取得"""
        return self.contract.functions.name().call()

    def mint_deposit(self):
        tx = self.contract.functions.mintDeposit().buildTransaction(
            {
                "nonce": self.network.eth.getTransactionCount(
                    self.contract_owner.address,
                ),
                "from": self.contract_owner.address,  # 自身のアドレスを含める
            }
        )
        tx_result = self.execute(tx)
        logger.info(f"{tx_result=}")

    def transfer(self, address, amount):
        """管理者アドレスのトークンを指定したユーザのアドレスに移管する"""
        tx = self.contract.functions.transfer(
            self.convert_checksum_address(address), amount
        ).buildTransaction(
            {
                "nonce": self.network.eth.getTransactionCount(
                    self.contract_owner.address,
                ),
                "from": self.contract_owner.address,  # 自身のアドレスを含める
            }
        )
        tx_result = self.execute(tx)
        logger.info(f"{tx_result=}")

    def transfer_to_vote_contract(self, amount):
        """投票用コントラクトにデポジットを送金する"""
        tx = self.contract.functions.transfer(
            self.convert_checksum_address(
                config.proposal_vote_contract_address
            ),
            amount,
        ).buildTransaction(
            {
                "nonce": self.network.eth.getTransactionCount(
                    self.contract_owner.address,
                ),
                "from": self.contract_owner.address,  # 自身のアドレスを含める
            }
        )
        tx_result = self.execute(tx)
        logger.info(f"{tx_result=}")

    def burn(self, address, amount):
        """ウォレットアドレスが所有しているトークンを削除する"""
        tx = self.contract.functions.burn(
            self.convert_checksum_address(address), amount
        ).buildTransaction(
            {
                "nonce": self.network.eth.getTransactionCount(
                    self.contract_owner.address,
                ),
                "from": self.contract_owner.address,  # 自身のアドレスを含める
            }
        )
        tx_result = self.execute(tx)
        logger.info(f"{tx_result=}")

    def balance_of_address(self, address):
        """ウォレットアドレスが所有しているトークン量を返す"""
        return self.contract.functions.balanceOf(
            self.convert_checksum_address(address)
        ).call()

    def balance_of_deposit(
        self,
    ):
        """供給可能なトークン量を確認する"""
        return self.contract.functions.balanceOfDeposit().call()
