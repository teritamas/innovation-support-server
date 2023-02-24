from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore

from app import config


class FireStore:
    def __init__(
        self,
        cred_path: str,
    ) -> None:
        cred = credentials.Certificate(cred_path)

        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        print("Fire Store: Initialize Complete!")

    def __call__(
        self,
    ) -> Any:
        return self.db


fire_store = FireStore(
    config.cred_path,
)
