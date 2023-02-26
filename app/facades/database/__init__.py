from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel

from app import config
from app.utils.logging import logger


class FireStore:
    def __init__(
        self,
        cred_path: str,
    ) -> None:
        cred = credentials.Certificate(cred_path)

        firebase_admin.initialize_app(cred)
        self._db = firestore.client()
        logger.info("Fire Store: Initialize Complete!")

    def __call__(
        self,
    ) -> Any:
        return self._db

    def add(self, collection: str, id: str, content: dict):
        doc_ref = self._db.collection(collection).document(id)
        doc_ref.set(content)

    def fetch(self, collection: str, id: str) -> dict:
        doc = self._db.collection(collection).document(id).get()
        return doc.to_dict()

    def delete(self, collection: str, id: str):
        self._db.collection(collection).document(id).delete()


fire_store = FireStore(
    config.cred_path,
)
