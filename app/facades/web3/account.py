import os
import secrets

from eth_account import Account

from app.utils.logging import logger


class ContractOwner:
    """スマートコントラクトを実行するウォレット"""

    def __init__(self, private_key_filename: str) -> None:
        self.private_key = self._load_private_key(private_key_filename)
        _account = Account.from_key(self.private_key)
        self.address = _account.address
        logger.info(f"Wallet Address: {self.address}")

    @staticmethod
    def _load_private_key(filename: str):
        """秘密鍵を読み込む。存在しない場合は生成する。

        Args:
            filename (str): 秘密鍵が保存されているパス。存在しない場合はそのパスに作成される。

        Returns:
            _type_: _description_
        """
        if os.path.exists(filename):
            with open(filename, "r") as fpr:
                private_key = fpr.read()
        else:
            logger.info(f"private key is not exists. create key. : {filename}")
            private_key = "0x" + secrets.token_hex(32)

            with open(filename, "w") as fpr:
                fpr.write(private_key)
        return private_key
