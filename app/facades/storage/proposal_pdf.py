from app.facades.storage import gcs
from app.utils.logging import logger

FOLDER_NAME = "ProposalAttachments"


def upload(data: bytes, destination_blob_name: str) -> str:
    blob = gcs().blob(f"{FOLDER_NAME}/{destination_blob_name}")
    generation_match_precondition = 0

    blob.upload_from_string(
        data,
        content_type="application/pdf",
        if_generation_match=generation_match_precondition,
    )

    logger.info(f"File uploaded to {destination_blob_name}.")


def download(destination_blob_name: str) -> bytes:
    blob = gcs().blob(f"{FOLDER_NAME}/{destination_blob_name}")

    return blob.download_as_bytes()


def delete(destination_blob_name: str):
    blob = gcs().blob(f"{FOLDER_NAME}/{destination_blob_name}")
    if blob.exists():
        blob.delete()
