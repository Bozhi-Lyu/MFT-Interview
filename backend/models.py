from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class StockPrice:
    """
    Represents the latest price snapshot of a stock.

    This model mirrors what a market-data event would look like
    in a real streaming system, simplified for this exercise.
    """

    sequence_id: int
    symbol: str
    name: str
    price: Decimal
    previous_close: Decimal
    currency: str
    updated_at: datetime

    def to_dict(self) -> dict:
        """
        Serialization in JSON.
        """
        abs_change = self.price - self.previous_close
        pct_change = (abs_change / self.previous_close) * Decimal("100") \
            if self.previous_close != Decimal("0") else Decimal("0")

        return {
            "sequence_id": self.sequence_id,
            "symbol": self.symbol,
            "name": self.name,
            "price": float(self.price),
            "abs_change": float(abs_change),
            "pct_change": float(pct_change),
            "currency": self.currency,
            "updated_at": self.updated_at.isoformat(),
        }
