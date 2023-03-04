import hashlib
import os
import uuid
from datetime import datetime, timedelta, timezone


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
