from app.schemas.proposal.requests import EntryProposalRequest
from app.schemas.proposal.responses import EntryProposalResponse


def execute(request: EntryProposalRequest):
    return EntryProposalResponse()


if __name__ == "__main__":
    execute(EntryProposalRequest())
