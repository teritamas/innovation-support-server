import base64
import hashlib
import os
import tempfile
import uuid
from datetime import datetime, timedelta, timezone

from pdf2image import convert_from_bytes
from PIL import Image


def now() -> datetime:
    return datetime.now(timezone(timedelta(hours=9)))


def timestamp_(dt: datetime):
    return datetime.timestamp(dt)


def timestamp_to_datetime(ts: float):
    return datetime.fromtimestamp(ts, timezone.utc)


def generate_id_str() -> str:
    return str(uuid.uuid4())


def build_nft_uri(user_id, proposal_id, filename) -> str:
    """nftに記録するファイルパスを指定する"""
    bucket_path = os.path.join(user_id, proposal_id, filename)
    hash_object = hashlib.md5(bucket_path.encode())
    nft_uri = f"{hash_object.hexdigest()}.pdf"
    return nft_uri


async def thumbnail_image_from_pdf(file) -> Image:
    data = await file.read()  # アップロードされた画像をbytesに変換する処理
    bin_data: bytes = base64.b64encode(data).decode()

    images = convert_from_bytes(
        data,
    )[0]
    return images
