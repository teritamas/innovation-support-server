from os import environ

from dotenv import load_dotenv

load_dotenv(verbose=True)

env = environ.get("ENV", "prd")

cred_path = environ.get("CRED_PATH", "")
google_cloud_storage_bucket_name = environ.get(
    "GOOGLE_CLOUD_STORAGE_BUCKET_NAME", ""
)
