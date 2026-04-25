# Jesse Bridge Plan

## Purpose

Bitcoin AI Lab currently runs as a browser-only GitHub Pages simulator. It uses synthetic Bitcoin markets, fake money, strategy personalities, a market-regime detector, an Adaptive Meta Bot, batch/tournament rankings, and local replay persistence.

Jesse is the larger Python trading framework that this repository was forked from. It should eventually provide the serious backtesting and trading-framework layer.

The bridge exists to connect those two worlds without breaking either one.

```text
Jesse backtest result
→ bridge adapter
→ Bitcoin AI Lab result JSON
→ browser lab scoreboard/replay UI
```

The first bridge target is not live trading. The first bridge target is backtest-result import.

## Current browser lab format

The browser lab already stores runs in this general shape:

```json
{
  "version": "v0.7",
  "savedAt": "2026-04-25T00:00:00.000Z",
  "mode": "selected",
  "bot": "meta",
  "botName": "Adaptive Meta Bot",
  "settings": {
    "start": 10000,
    "seed": 42,
    "market": "mixed",
    "fee": 0.001,
    "slip": 0.0005,
    "steps": 240,
    "vol": 1
  },
  "summary": {
    "finalValue": 11420,
    "returnPct": 14.2,
    "maxDrawdownPct": -12.83,
    "trades": 37,
    "fees": 24,
    "slippage": 12,
    "beatHold": true,
    "regime": "Uptrend",
    "regimeConfidence": "Medium"
  },
  "replay": []
}
```

The bridge should output this same style of object, even if the source was Jesse instead of the browser simulator.

## Jesse capabilities wanted later

Jesse can potentially provide:

- historical candle backtests
- real trading-pair/timeframe structure
- strategy classes
- indicator support
- metrics and statistics
- trade logs
- equity curves
- optimization and Monte Carlo tooling
- paper/live architecture later

For Bitcoin AI Lab, the first useful Jesse capabilities are:

1. Backtest execution
2. Trade/equity result extraction
3. Metrics extraction
4. Strategy-to-lab mapping
5. Historical candle support

Live trading is explicitly out of scope for the first bridge.

## Bridge architecture

```text
Bitcoin AI Lab Browser UI
  - scoreboard
  - replay table
  - batch/tournament display
  - local storage
  - import/export JSON

Bridge Result Format
  - stable JSON schema
  - engine-agnostic
  - can come from synthetic simulator or Jesse

Jesse Adapter
  - runs or reads Jesse backtest results
  - extracts equity/trades/metrics
  - maps them into bridge result format

Jesse Engine
  - Python strategy/backtest framework
  - not bundled inside GitHub Pages
```

The browser lab should not need to know whether a result came from:

- the current synthetic simulator
- a Jesse backtest
- a future paper-trading session
- a future guarded live run

It should just render a standard lab result object.

## Bridge input schema

A future Jesse bridge request should look roughly like this:

```json
{
  "engine": "jesse",
  "mode": "backtest",
  "exchange": "Binance",
  "symbol": "BTC-USDT",
  "timeframe": "1h",
  "startDate": "2023-01-01",
  "endDate": "2024-01-01",
  "strategy": "TrendHunter",
  "startingBalance": 10000,
  "feePct": 0.1,
  "slippagePct": 0.05,
  "liveTradingAllowed": false
}
```

Required fields for v0.9 prototype:

- engine
- mode
- symbol
- timeframe
- strategy
- starting balance
- fee/slippage settings

Fields that can wait:

- exchange-specific config
- real candle import path
- optimization config
- paper trading session metadata
- API credentials

## Bridge output schema

A Jesse-backed lab result should output:

```json
{
  "version": "bridge-v0.1",
  "engine": "jesse",
  "mode": "backtest",
  "bot": "trend",
  "botName": "Trend Hunter",
  "settings": {
    "exchange": "Binance",
    "symbol": "BTC-USDT",
    "timeframe": "1h",
    "startDate": "2023-01-01",
    "endDate": "2024-01-01",
    "startingBalance": 10000,
    "fee": 0.001,
    "slip": 0.0005
  },
  "summary": {
    "finalValue": 12500,
    "returnPct": 25,
    "maxDrawdownPct": -18.5,
    "trades": 52,
    "fees": 143,
    "slippage": 0,
    "beatHold": false,
    "regime": "Historical",
    "regimeConfidence": "N/A"
  },
  "equity": [
    { "time": "2023-01-01T00:00:00Z", "value": 10000 },
    { "time": "2023-01-02T00:00:00Z", "value": 10080 }
  ],
  "trades": [
    {
      "time": "2023-01-03T00:00:00Z",
      "side": "buy",
      "price": 16750,
      "qty": 0.1,
      "fee": 1.67,
      "reason": "Strategy opened long"
    }
  ],
  "replay": [
    [1, 16750, "BUY", "Strategy opened long", 10000]
  ],
  "warnings": []
}
```

The browser renderer should care most about:

- `summary.finalValue`
- `summary.returnPct`
- `summary.maxDrawdownPct`
- `summary.trades`
- `summary.fees`
- `summary.beatHold`
- `replay`
- `equity`

## Safe Jesse areas to inspect

Before any code bridge, inspect Jesse for these areas:

```text
backtest
routes
strategy
candles
trades
orders
metrics
statistics
store
config
research
```

Likely questions:

1. Where does Jesse start a backtest?
2. Where are routes/strategies configured?
3. Where are candles loaded/imported?
4. Where are trades stored during a run?
5. Where is equity curve or portfolio value calculated?
6. Where are metrics/statistics emitted?
7. Can we run a backtest without touching live/paper execution?
8. Can we export a JSON result without altering Jesse internals?

## Non-goals for the first bridge

Do not do these in the first bridge:

- do not add exchange keys
- do not enable live trading
- do not enable paper trading yet
- do not rename the full Jesse package
- do not move large Jesse directories
- do not force Jesse into GitHub Pages
- do not make Android/APK packaging part of this step
- do not use OpenAI API calls in the bridge

The first bridge should be boring: result format, import/export, and safe backtest mapping.

## Safety gates

Default rule:

```text
ALLOW_REAL_MONEY_TRADING = false
```

Bridge v1 rule:

```text
Jesse bridge v1 = backtest import only
```

Before anything real-money-related exists, the project must have:

- explicit live-trading unlock
- separate execution layer
- max position size
- max daily loss
- emergency stop
- visible warning state
- no credentials in GitHub Pages
- no credentials committed to repo

## v0.9 prototype plan

The safest next prototype is not to run Jesse yet.

The safest next prototype is:

```text
Import Result JSON
```

Steps:

1. Add a browser-lab import area/button.
2. Paste or load a bridge-format JSON result.
3. Render it in the same scoreboard/replay UI.
4. Confirm the browser lab can display engine-agnostic results.
5. Then inspect Jesse internals for actual extraction points.

That proves the adapter contract before Python integration.

## v1.0 bridge prototype plan

After the browser can import result JSON:

1. Inspect Jesse backtest flow.
2. Create a small adapter script outside Jesse internals.
3. Run or read a Jesse backtest result.
4. Export bridge-format JSON.
5. Paste/import that JSON into the browser lab.
6. Compare with synthetic lab results.

## Current bridge stance

Jesse is the future serious engine.

The browser lab is the fast Android-visible interface.

The bridge format is the contract between them.

Do not merge the layers until the contract is proven.