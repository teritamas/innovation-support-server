import json

from web3 import Web3

from app.facades.web3.account import ContractOwner


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

        # 所有者でないと実行できない為
        # if self.owner() == self.contract_owner:
        #     RuntimeError

    def getTokenIdByTransactionLog(self, logs) -> int:
        """トランザクションログからTokenIdを検索する. TODO: 改善の必要あり"""
        tokenId = int(logs[-1]["topics"][-1].hex().replace("0x", ""), base=16)
        return tokenId

    async def mint(self, proposer_address: str, identifier: str) -> str:
        """提案NFTを発行し提案者のウォレットにNFTを紐づける

        Args:
            proposer_address (str): 提案者のウォレットアドレス
            identifier (str): 識別子
        """
        tx = self.contract.functions.nftMint(
            proposer_address, identifier
        ).buildTransaction(
            {
                "nonce": self.network.eth.getTransactionCount(
                    self.contract_owner.address
                )
            }
        )
        tx_result = self.execute(tx)
        tokenId = self.getTokenIdByTransactionLog(tx_result["logs"])
        return tokenId

    def vote(self, target_nft_id: str, voter_address: str, token_amount: int):
        """提案に対して投票をし、その見返りに投票者にトークンを発行する。

        Args:
            target_nft_id (str): 投票するNFTのId
            voter_address (str): 投票者のウォレットアドレス
            token_amount (int): 発行するトークン量
        """
        # TODO: 提案に対して投票を行い、投票者にトークンを発行するコントラクトの作成
        print(
            f"vote proposal nft. {target_nft_id=}, {voter_address=}, {token_amount=}"
        )

    def burn(self, wallet_address: str, burn_token_amount: int):
        """トークンを消費する。トークンを消費して、福利厚生や研修プロジェクトを受けるユースケースまで実装する場合に実装する。

        Args:
            wallet_address (str): _description_
            burn_token_amount (int): _description_
        """
        # TODO: トークンを焼却する
        print(f"burn token. {wallet_address=}, {burn_token_amount=}")


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
