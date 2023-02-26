import hashlib
import os
import uuid


def generate_id_str() -> str:
    return str(uuid.uuid4())


def build_nft_uri(user_id, proposal_id, filename) -> str:
    """nftに記録するファイルパスを指定する"""
    bucket_path = os.path.join(user_id, proposal_id, filename)
    hash_object = hashlib.md5(bucket_path.encode())
    nft_uri = f"{hash_object.hexdigest()}.pdf"
    return nft_uri
