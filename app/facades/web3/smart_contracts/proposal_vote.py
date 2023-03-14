from app.facades.web3.account import ContractOwner
from app.facades.web3.smart_contracts.base_contract import BaseContract
from app.schemas.proposal_vote.domain import ProposalVoteOnContract
from app.utils.logging import logger


class ProposalVoteContract(BaseContract):
    """投票用のコントラクト"""

    def __init__(
        self,
        contract_owner: ContractOwner,
        contract_address: str,
        proposal_nft_contract_address: str,
        inosapo_ft_contract_address: str,
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

        self._set_relate_contract(
            proposal_nft_contract_address, inosapo_ft_contract_address
        )

    def _set_relate_contract(
        self, proposal_nft_contract_address, inosapo_ft_contract_address
    ):
        # 提案NFTを設定
        if (
            self.contract.functions.getNftContractAddress().call()
            != proposal_nft_contract_address
        ):
            logger.info(f"Set ProposalNFT address")
            tx = self.contract.functions.setNftContractAddress(
                proposal_nft_contract_address
            ).buildTransaction(
                {
                    "nonce": self.network.eth.getTransactionCount(
                        self.contract_owner.address,
                    ),
                    "from": self.contract_owner.address,  # 自身のアドレスを含める
                }
            )
            tx_result = self.execute(tx)
            logger.info(tx_result)

        # トークン発行用コントラクトを設定
        if (
            self.contract.functions.getERC20ContractAddress().call()
            != inosapo_ft_contract_address
        ):
            logger.info(f"Set InosapoFT address")
            tx = self.contract.functions.setERC20ContractAddress(
                inosapo_ft_contract_address
            ).buildTransaction(
                {
                    "nonce": self.network.eth.getTransactionCount(
                        self.contract_owner.address,
                    ),
                    "from": self.contract_owner.address,  # 自身のアドレスを含める
                }
            )
            tx_result = self.execute(tx)
            logger.info(tx_result)

    def entry_proposal(self, tokenId):
        tx = self.contract.functions.entryProposal(tokenId).buildTransaction(
            {
                "nonce": self.network.eth.getTransactionCount(
                    self.contract_owner.address,
                ),
                "from": self.contract_owner.address,  # 自身のアドレスを含める
            }
        )
        tx_result = self.execute(tx)
        logger.info(f"{tx_result=}")

    def vote(self, tokenId: int, voterAddress: str, judgement: bool):
        tx = self.contract.functions.vote(
            tokenId, self.convert_checksum_address(voterAddress), judgement
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

    def judgement_proposal(self, tokenId: int, judgement: bool):
        tx = self.contract.functions.judgementProposal(
            tokenId, judgement
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

    def get_status(self, tokenId: int) -> ProposalVoteOnContract:
        """投票ステータスを取得

        Args:
            tokenId (int): 対象のトークンID

        Returns:
            ProposalVoteOnContract: _description_
        """
        result_list = self.contract.functions.proposals(tokenId).call()
        return ProposalVoteOnContract(
            address=result_list[0],
            vote_total_count=result_list[1],
            vote_agreement_count=result_list[2],
            voting_status=result_list[3],
        )
