import json
from typing import List

import requests


def broadcast(
    incoming_webhooks_url: str,
    channels: List[str],
    proposal_view_url: str,
):
    for channel in channels:
        payload = {
            "channel": f"#{channel}",
            "username": "いのさぽくん",
            "text": f"新しいアイデアが投稿されました! 下記のURLから確認してください!\n{proposal_view_url}",
            "icon_emoji": ":bulb:",
        }

        json_payload = json.dumps(payload)
        data = {"payload": json_payload}

        response = requests.post(
            incoming_webhooks_url,
            data=data,
        )
        print(f"notification result. {channel=}, {response=}")
