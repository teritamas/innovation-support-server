from web3 import Web3

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

    def fetchTokenInfoByTokeId(self, tokenId: int):
        """トークンIDからNFTのURIを取得する"""
        return self.contract.functions.tokenURI(tokenId).call()

    def getTokenIdByTransactionLog(self, logs) -> int:
        """トランザクションログからTokenIdを検索する. TODO: 改善の必要あり"""
        tokenId = int(logs[-1]["topics"][-1].hex().replace("0x", ""), base=16)
        return tokenId

    def mint(self, proposer_address: str, identifier: str, amount: int) -> str:
        """提案NFTを発行し提案者のウォレットにNFTを紐づける

        Args:
            proposer_address (str): 提案者のウォレットアドレス
            identifier (str): 識別子
            amount(int):この提案で受け取りたいトークン量
        """
        logger.info(
            f"提案をNFT化します. {proposer_address=}, {identifier=}, {amount=}"
        )
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
        logger.info(f"提案のNFTの登録が完了しました. {tx_result=}")
        tokenId = self.getTokenIdByTransactionLog(tx_result["logs"])
        logger.info(f"提案のNFTのトークンIDの取得が完了しました. {tokenId=}")
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
