# Case

```
## Stock Price Ticker View

You're tasked with making a "frontend/client" and "backend/server" application, which displays Stock Prices. 
You should not spend more than 1-2 hours on this, as it only serves as a common talking point. Furthermore, there will be no penalty for not finishing the assignment completely, as mentioned before, its just a common talking point.

We would prefer you solve the excercise using C# and .NET Core or Python.

## Requirements are as follows:

- Stock Price Model:
  - Should have a price with decimal support
  - Should have a Name, eg: Google, Apple, Microsoft, Berkshire etc.
  - Extend with extra information, if you have the time, but not needed.
  - Generated Prices do not need to look "real"(random prices are sufficient).

- Frontend/Client:
  - Should receive "Stock Price Models" from the backend.
  - These prices should be displayed in a human readable format
  - This can just be something as simple as a console application

- Backend/Server
  - Generate "Stock Price Models" every 1-2 seconds.
  - The generated "Stock Price Models" should be the same set of Stocks (Apple, Google, Microsoft etc.) every time
  - Send the generated prices to the frontend using network communication
```

# System Design
This is a **minimal client–server system** simulating a **real-time market data feed**.

The backend periodically generates price updates for a fixed set of stocks and **streams snapshots to connected clients via WebSocket**.
The design intentionally mirrors a **simplified event-driven architecture** commonly used in production market-data and streaming systems.

The focus of the exercise is **data flow**, **system boundaries**, and **real-time communication**, rather than financial realism.

## Stock Price Model
The stock price model is designed to resemble a market-data event schema in real systems.

### data model: 
Each stock price snapshot contains:
- `name`, string
- `symbol`, string
- `Price`, decimal (avoid precision issues)
- `previous_close`, decimal, Fixed reference price
- `abs_change`, derived
- `pct_change`, derived
- `updated_at`, timestamp
- `currency`, string
- `sequence_id`, int for ordering

### data source

Prices are generated using a bounded random walk (±0.5%) applied to the current price at a fixed interval (default: 1 second).

The `previous_close` value is initialized at startup and remains constant.

### State management
- All state is kept in memory for this exercise.
- No persistence is used for now, to keep the system focused on streaming and communication.
- In a production system, this state could come from:
    - A market data provider
    - A message broker (Kafka / Redis Streams)
    - A time-series database

## Server 
The backend is implemented as a single-process FastAPI application with clear internal separation of concerns: **price generation (ingestion)**; **state management**; **distribution**.

- Periodically update dummy prices using the generator.
- Maintain a fixed universe of stocks (hardcoded at startup, e.g. ["AAPL", "GOOG", "MSFT"]).
- Compute derived metrics
- Broadcast the latest snapshot to all connected clients via WebSocket

## Client
The client is a stateless and passive console application, responsible for connecting to the WebSocket endpoint and receiving streaming snapshots, and rendering.

# API Definition

Protocol: WebSocket(server → client streaming)

Serialization: JSON

Message semantics: Each message represents a snapshot of all tracked stocks at a given point in time.

``` Json
{
  "type": "stock_price_update",
  "timestamp": "2026-02-02T12:00:01Z",
  "data": [
    {
      "symbol": "AAPL",
      "name": "Apple",
      "price": 187.32,
      "abs_change": 4.50,
      "pct_change": 2.41,
      "currency": "USD",
      "updated_at": "2026-02-02T12:00:01Z",
      "sequence_id": 16
    },
    {
      "symbol": "GOOG",
      "name": "Google",
      "price": 134.58,
      "abs_change": -0.91,
      "pct_change": -0.67,
      "currency": "USD",
      "updated_at": "2026-02-02T12:00:01Z",
      "sequence_id": 17
    }
  ]
}
```

## Notes on Production Mapping

WebSocket streaming simulates a real-time market data feed. In production:
- Price generation would be replaced by ingestion from an external source
- In-memory state would be replaced by a distributed state store or event stream
- Multiple WebSocket workers would subscribe to a shared stream for horizontal scaling
- Authentication, reconnection, etc.