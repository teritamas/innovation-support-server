import os

from PIL import Image

from app.facades.storage import gcs
from app.utils.logging import logger

FOLDER_NAME = "ProposalThumbnailImages"
TEMP_FOLDER_NAME = "./temp/thumbnail"


def upload(
    destination_blob_name: str,
    image: Image,
) -> str:
    temp_image_filename = _save_temp_image(destination_blob_name, image)
    try:
        blob = gcs().blob(f"{FOLDER_NAME}/{destination_blob_name}")

        blob.upload_from_filename(
            temp_image_filename,
        )

        logger.info(f"File uploaded to {destination_blob_name}.")
    except Exception as e:
        logger.error(f"upload error. {e}")
    finally:
        os.remove(temp_image_filename)


def _save_temp_image(destination_blob_name, image):
    """アップロードのため一時的にローカルに保存する"""
    os.makedirs(TEMP_FOLDER_NAME, exist_ok=True)
    temp_image_filename = f"{TEMP_FOLDER_NAME}/{destination_blob_name}"
    image.save(temp_image_filename)
    return temp_image_filename


def download(destination_blob_name: str) -> bytes:
    blob = gcs().blob(f"{FOLDER_NAME}/{destination_blob_name}")

    return blob.download_as_bytes()


def delete(destination_blob_name: str):
    blob = gcs().blob(f"{FOLDER_NAME}/{destination_blob_name}")
    if blob.exists():
        blob.delete()
