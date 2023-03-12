from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.base_contract import BaseContract
from app.utils.logging import logger


class ProposalNFT(BaseContract):
    """提案NFTのコントラクト"""

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

    def fetchTokenInfoByTokeId(self, tokenId: int):
        """トークンIDからNFTのURIを取得する"""
        return self.contract.functions.tokenURI(tokenId).call()

    def getTokenIdByTransactionLog(self, logs) -> int:
        """トランザクションログからTokenIdを検索する. TODO: 改善の必要あり"""
        tokenId = int(logs[-1]["topics"][-1].hex().replace("0x", ""), base=16)
        return tokenId

    async def mint(
        self, proposer_address: str, identifier: str, amount: int
    ) -> str:
        """提案NFTを発行し提案者のウォレットにNFTを紐づける

        Args:
            proposer_address (str): 提案者のウォレットアドレス
            identifier (str): 識別子
            amount(int):この提案で受け取りたいトークン量
        """
        tx = self.contract.functions.mintNft(
            self.convert_checksum_address(proposer_address), identifier, amount
        ).buildTransaction(
            {
                "nonce": self.network.eth.getTransactionCount(
                    self.contract_owner.address
                ),
                "from": self.contract_owner.address,  # 自身のアドレスを含める
            }
        )
        tx_result = self.execute(tx)
        tokenId = self.getTokenIdByTransactionLog(tx_result["logs"])
        return tokenId

    def get_token_amount(self, tokenId):
        """NFTに紐づく調達額を確認する"""
        return self.contract.functions.getTokenAmount(tokenId).call()

    def burn(self, wallet_address: str, burn_token_amount: int):
        """トークンを消費する。トークンを消費して、福利厚生や研修プロジェクトを受けるユースケースまで実装する場合に実装する。

        Args:
            wallet_address (str): _description_
            burn_token_amount (int): _description_
        """
        # TODO: トークンを焼却する
        logger.info(f"burn token. {wallet_address=}, {burn_token_amount=}")
