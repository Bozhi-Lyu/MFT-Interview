import random
from decimal import Decimal
from .registry import StockRegistry

class PriceGenerator:
    """
    Applies bounded random price movements to all stocks in the registry on each tick.
    Simulates a simplified market data feed.
    """

    def __init__(
        self,
        registry: StockRegistry,
        max_change_pct: Decimal = Decimal("0.005"),
    ) -> None:
        """
        :param registry: In-memory stock registry
        :param max_change_pct: Maximum percentage price change per tick
        """
        self._registry = registry
        self._max_change_pct = max_change_pct

    def tick(self) -> None:
        for stock in self._registry.get_all():
            delta_pct = Decimal(
                random.uniform(
                    float(-self._max_change_pct),
                    float(self._max_change_pct),
                )
            )

            new_price = stock.price * (Decimal("1.0") + delta_pct)

            if new_price <= Decimal("0"):
                continue

            # Normalize to 2 decimal places
            new_price = new_price.quantize(Decimal("0.01"))

            self._registry.update_price(stock.symbol, new_price)
