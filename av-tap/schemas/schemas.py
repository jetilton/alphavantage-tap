from typing import List
import datetime
from pydantic import BaseModel


class DailyAdjustedItemModel(BaseModel):
    date_time: datetime.date
    symbol: str
    open: float
    high: float
    low: float
    close: float
    adjusted_close: float
    volume: int
    dividend_amount: float
    split_coefficient: float


class DailyAdjustedModel(BaseModel):
    data: List[DailyAdjustedItemModel]


if __name__ == "__main__":
    for k, v in {"daily_adjusted": DailyAdjustedModel}.items():
        with open(f"./av-tap/schemas/{k}.json", "w") as f:
            f.write(DailyAdjustedModel.schema_json(indent=2))
