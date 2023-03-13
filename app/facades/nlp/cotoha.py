import collections
import itertools
import os

import requests


class CotohaFacade:
    def __init__(self, client_id: str, client_secret: str):
        self.base_url = "https://api.ce-cotoha.com/api/dev/"
        self.is_active = False
        try:
            self.access_token = self._create_access_token(
                client_id, client_secret
            )
            self.is_active = True
        except Exception as e:
            print(e)

    def _create_access_token(self, client_id: str, client_secret: str) -> str:
        """CotohaAPIを利用するためのアクセストークンを取得する。
        Args:
            client_id (str): [description]
            client_secret (str): [description]
        Returns:
            str: [description]
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }
        body = {
            "grantType": "client_credentials",
            "clientId": client_id,
            "clientSecret": client_secret,
        }
        response = requests.post(
            "https://api.ce-cotoha.com/v1/oauth/accesstokens",
            headers=headers,
            json=body,
        )
        return response.json()["access_token"]

    def predict(self, target_sentence: str) -> dict:
        """Cotohaの感情分析APIを利用する。
        https://api.ce-cotoha.com/contents/reference/apireference.html#similarity
        Args:
            target_sentence (str): The sentence to be identified
        Returns:
            str: Json string containing the identification results
        """

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": "Bearer " + self.access_token,
        }
        body = {"sentence": target_sentence}

        endpoint = os.path.join(self.base_url, "nlp/v1/sentiment")
        cotoha_response = requests.post(endpoint, headers=headers, json=body)
        if cotoha_response.json()["result"]["emotional_phrase"] != []:
            tmp_cotoha_response_array = [
                x["emotion"].split(",")
                for x in cotoha_response.json()["result"]["emotional_phrase"]
            ]
            cotoha_response_array = list(
                itertools.chain.from_iterable(tmp_cotoha_response_array)
            )
            emotional_sentiment = self._get_max_emotion(cotoha_response_array)
        else:
            emotional_sentiment = cotoha_response.json()["result"]["sentiment"]
        response = cotoha_response.json()
        response["result"]["emotional_sentiment"] = emotional_sentiment

        return response

    def _get_max_emotion(self, emotion_list: list) -> str:
        counter = collections.Counter(emotion_list)
        emotion_value = counter.most_common()[0][0]
        if emotion_value == "P":
            return "Positive"
        elif emotion_value == "PN":
            return "Neutral"
        elif emotion_value == "N":
            return "Negative"
        else:
            return emotion_value

    def keyword(self, target_sentence: str, threshold: float = 0) -> list[str]:
        """文章のキーワードを抽出する。
        Args:
            target_sentence (str): _description_
        """
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": "Bearer " + self.access_token,
        }
        body = {
            "document": target_sentence,
            "type": "default",
            "max_keyword_num": 3,
            "dic_type": "medical",
        }

        endpoint = os.path.join(self.base_url, "nlp/v1/keyword")
        cotoha_response = requests.post(endpoint, headers=headers, json=body)

        results = cotoha_response.json()["result"]
        if results == []:
            return []

        keywords = []
        for result in results:
            keywords.append(result.get("form"))

        return keywords
