import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .registry import StockRegistry
from .generator import PriceGenerator
from .stream import PriceStreamService

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(price_update_loop())
    try:
        yield
    finally:
        task.cancel()

app = FastAPI(title="Stock Price Ticker", lifespan=lifespan)
registry = StockRegistry()
generator = PriceGenerator(registry)
stream_service = PriceStreamService(registry)


async def price_update_loop(interval_seconds: float = 1.0) -> None:
    """
    Background task that periodically updates prices
    and broadcasts snapshots to connected clients.
    """
    while True:
        generator.tick()
        await stream_service.broadcast()
        await asyncio.sleep(interval_seconds)

@app.websocket("/ws/prices")
async def prices_websocket(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for streaming stock price updates.
    """
    await stream_service.register(websocket)

    try:
        while True:  # Keep the connection open
            await websocket.receive_text()  # Server is push-only
    except WebSocketDisconnect:  # Safe disconnect
        await stream_service.unregister(websocket)
