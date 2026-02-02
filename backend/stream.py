import json
from datetime import datetime, timezone
from typing import Set

from fastapi import WebSocket

from .registry import StockRegistry


class PriceStreamService:
    """
    Manages WebSocket clients and broadcasts stock price snapshots.
    """

    def __init__(self, registry: StockRegistry) -> None:
        self._registry = registry
        self._clients: Set[WebSocket] = set()

    async def register(self, websocket: WebSocket) -> None:
        """
        Accept and register a new WebSocket client.
        """
        await websocket.accept()
        self._clients.add(websocket)

    async def unregister(self, websocket: WebSocket) -> None:
        """
        Remove a disconnected WebSocket client.
        """
        self._clients.discard(websocket)

    async def broadcast(self) -> None:
        """
        Broadcast the latest stock price snapshot to all clients.
        """
        if not self._clients:
            return

        message = {
            "type": "stock_price_update",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": [
                stock.to_dict()
                for stock in self._registry.get_all()
            ],
        }

        payload = json.dumps(message)

        dead_clients = set()

        for client in self._clients:
            try:
                await client.send_text(payload)
            except Exception:
                dead_clients.add(client)

        # Clean up dead connections
        for client in dead_clients:
            self._clients.discard(client)
