from os import environ

from dotenv import load_dotenv

load_dotenv(verbose=True)

env = environ.get("ENV", "prd")

cred_path = environ.get("CRED_PATH", "")
google_cloud_storage_bucket_name = environ.get(
    "GOOGLE_CLOUD_STORAGE_BUCKET_NAME", ""
)

provider_network = environ.get("PROVIDE_NETWORK", "")
proposal_nft_contract_address = environ.get(
    "PROPOSAL_NFT_CONTRACT_ADDRESS", ""
)
system_wallet_private_key_path = environ.get(
    "SYSTEM_WALLET_PRIVATE_KEY_PATH", ""
)
