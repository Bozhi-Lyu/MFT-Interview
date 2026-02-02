import asyncio
import json
import os
from datetime import datetime

import websockets


WS_URL = "ws://localhost:8000/ws/prices"


def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_snapshot(message: dict) -> None:
    clear_console()

    timestamp = message.get("timestamp")
    ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    formatted_ts = ts.strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"Stock Prices @ {formatted_ts}")

    print("-" * 60)
    print(f"{'Symbol':<8} {'Name':<15} {'Price':>10} {'Δ':>10} {'Δ%':>8}")
    print("-" * 60)

    for stock in message.get("data", []):
        abs_change = stock["abs_change"]
        pct_change = stock["pct_change"]

        print(
            f"{stock['symbol']:<8} "
            f"{stock['name']:<15} "
            f"{stock['price']:>10.2f} "
            f"{abs_change:>+10.2f} "
            f"{pct_change:>+8.2f}%"
        )


async def run_client() -> None:
    async with websockets.connect(WS_URL) as websocket:
        async for raw_message in websocket:
            message = json.loads(raw_message)

            if message.get("type") == "stock_price_update":
                render_snapshot(message)


if __name__ == "__main__":
    asyncio.run(run_client())
