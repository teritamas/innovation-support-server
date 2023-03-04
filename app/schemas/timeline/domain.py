from typing import List

from pydantic import BaseModel, Field

from app.utils.common import now, timestamp_


class Timeline(BaseModel):
    timestamp: float = Field(timestamp_(now()), description="取得時間")
    timelines: List = Field([], description="最近のアクション")
