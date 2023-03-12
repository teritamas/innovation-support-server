from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.base_contract import BaseContract


class SampleNFT(BaseContract):
    """FIXME: サンプル用途. 将来的に削除する."""

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
