import asyncio
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.schemas.proposal.domain import (
    JudgementStatusDto,
    Proposal,
    ProposalStatus,
)
from app.services.proposal import (
    find_proposal_service,
    judgement_proposal_service,
)
from app.utils.logging import logger


async def main():
    voting_proposals: List[Proposal] = find_proposal_service.execute(
        proposal_status=ProposalStatus.VOTING
    )
    logger.info(f"Target lists. {voting_proposals=}")

    for proposal in voting_proposals:
        logger.info(f"{'=' * 100}")
        try:
            status: JudgementStatusDto = (
                await judgement_proposal_service.execute(
                    proposal_id=proposal.proposal_id
                )
            )
            logger.info(
                f"Check Complete! {proposal.title=}, {status.proposal_status=}"
            )

        except Exception as e:
            logger.warn(f"This id missed. {proposal.proposal_id=}. {e=}")


if __name__ == "__main__":
    asyncio.run(main())
