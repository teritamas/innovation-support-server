from app.facades.gcs import gcs


def upload(data: bytes, destination_blob_name: str) -> str:
    blob = gcs().blob(destination_blob_name)
    generation_match_precondition = 0

    blob.upload_from_string(
        data,
        content_type="application/pdf",
        if_generation_match=generation_match_precondition,
    )

    print(f"File uploaded to {destination_blob_name}.")


def download(destination_blob_name: str) -> bytes:
    blob = gcs().blob(destination_blob_name)

    return blob.download_as_bytes()


def delete(destination_blob_name: str):
    blob = gcs().blob(destination_blob_name)
    if blob.exists():
        blob.delete()
