import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.facades.database import proposal_votes_store, users_store
from app.schemas.proposal_vote.domain import ProposalVote
from app.schemas.user.domain import User
from app.utils.common import now


def add_vote_user(user_id: str):
    users_store.add_user(
        id=user_id,
        content=User(
            user_id=user_id,
            user_name="vote_user",
            wallet_address="0x999050DBCD3a7fDBcF1204201587797D1849AC97",  # テストユーザ2のウォレットアドレス
        ),
    )


def add_vote(
    proposal_id: str,
    user_id: str,
    judgement: bool,
    message: str = "これはテストスクリプトから投票されました。",
):
    mint_token_amount = 10
    proposal_votes_store.add_proposal_vote(
        proposal_id,
        ProposalVote(
            user_id=user_id,
            mint_token_amount=mint_token_amount,
            judgement=judgement,
            judgement_reason=message,
            created_at=now(),
            updated_at=now(),
        ),
    )


def main(proposal_id: str, voter_count: int, agreement_rate: float):
    agreement_voter_count = int(agreement_rate * voter_count)
    disagreement_voter_count = voter_count - agreement_voter_count
    print(
        f"投票総数: {voter_count}, 賛成:反対/{agreement_voter_count}:{disagreement_voter_count}"
    )

    # 承認の投票を行う。
    for agreement_voter_index in range(agreement_voter_count):
        user_id: str = f"positive_user_{agreement_voter_index}"
        add_vote_user(user_id=user_id)
        add_vote(proposal_id=proposal_id, user_id=user_id, judgement=True)
        print(f"Positive User Insert: {user_id}")

    # 否決の投票を行う
    for disagreement_voter_count in range(disagreement_voter_count):
        user_id: str = f"negative_user_{disagreement_voter_count}"
        add_vote_user(user_id=user_id)
        add_vote(proposal_id=proposal_id, user_id=user_id, judgement=False)
        print(f"Negative User Insert: {user_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--proposal_id", type=str, help="投票対象の提案ID")
    parser.add_argument("--voter_count", default=100, type=int, help="投票数")
    parser.add_argument(
        "--agreement_rate", default=0.7, type=float, help="賛成の割合"
    )
    args = parser.parse_args()
    main(
        proposal_id=args.proposal_id,
        voter_count=args.voter_count,
        agreement_rate=args.agreement_rate,
    )
