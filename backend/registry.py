from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, List

from .models import StockPrice

class StockRegistry:
    """
    In-memory registry holding the latest price snapshot for a fixed set of stocks.
    Serves as the single source of truth for prices.
    """

    def __init__(self) -> None:
        self._sequence_counter: int = 0
        self._stocks: Dict[str, StockPrice] = {}
        self._initialize_stocks()

    def _initialize_stocks(self) -> None:
        initial_data = [
            ("AAPL", "Apple", Decimal("187.00")),
            ("GOOG", "Google", Decimal("134.00")),
            ("MSFT", "Microsoft", Decimal("412.00")),
            ("AMZN", "Amazon", Decimal("98.00")),
            ("TSLA", "Tesla", Decimal("256.00")),
        ]

        now = datetime.now(timezone.utc)

        for symbol, name, price in initial_data:
            self._sequence_counter += 1
            self._stocks[symbol] = StockPrice(
                symbol=symbol,
                name=name,
                price=price,
                previous_close=price,
                currency="USD",
                updated_at=now,
                sequence_id=self._sequence_counter,
            )

    def get_all(self) -> List[StockPrice]:
        """
        Return all current stock price snapshots.
        """
        return list(self._stocks.values())

    def update_price(self, symbol: str, new_price: Decimal) -> None:
        """
        Update the price of a single stock and advance sequence id.
        """
        if symbol not in self._stocks:
            raise KeyError(f"Unknown stock symbol: {symbol}")

        self._sequence_counter += 1

        stock = self._stocks[symbol]
        stock.price = new_price
        stock.updated_at = datetime.now(timezone.utc)
        stock.sequence_id = self._sequence_counter
