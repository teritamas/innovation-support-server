from os import environ

from dotenv import load_dotenv

load_dotenv(verbose=True)

"""
必須
"""
cred_path = environ.get("CRED_PATH", "")
if cred_path == "":
    print(f"CRED_PATH is required. {cred_path=}")
    exit()

proposal_nft_contract_address = environ.get(
    "PROPOSAL_NFT_CONTRACT_ADDRESS", ""
)
if proposal_nft_contract_address == "":
    print(
        f"PROPOSAL_NFT_CONTRACT_ADDRESS is required. {proposal_nft_contract_address=}"
    )
    exit()

inosapo_ft_contract_address = environ.get("INOSAPO_FT_CONTRACT_ADDRESS", "")
if inosapo_ft_contract_address == "":
    print(
        f"INOSAPO_FT_CONTRACT_ADDRESS is required. {inosapo_ft_contract_address=}"
    )
    exit()

"""
必要に応じて設定
"""
system_wallet_private_key_path = environ.get(
    "SYSTEM_WALLET_PRIVATE_KEY_PATH", "./key/system_private.key"
)  # 本システムのウォレットの秘密鍵、指定しない場合は指定したパスに自動で生成される。
provider_network = environ.get(
    "PROVIDE_NETWORK", "https://goerli.blockpi.network/v1/rpc/public"
)  # 上記のコントラクトをデプロイしたネットワーク名

google_cloud_storage_bucket_name = environ.get(
    "GOOGLE_CLOUD_STORAGE_BUCKET_NAME", "innovation-support-server"
)  # 提案を保存する場合の、Google Cloud Storageのバケット名

# 環境情報
env = environ.get("ENV", "dev")
frontend_url = environ.get("FRONTEND_URL", "http://0.0.0.0:3000")

# Slack通知を利用する場合、通知先のSlackのIncoming WebhooksのURL
default_slack_incoming_webhooks_url = environ.get(
    "DEFAULT_SLACK_INCOMING_WEBHOOKS_URL", ""
)
