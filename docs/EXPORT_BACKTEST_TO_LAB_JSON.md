# Export Jesse Backtest to Bitcoin AI Lab JSON

## Purpose

This document explains how to use:

```text
scripts/export_backtest_session_to_lab_json.py
```

The exporter converts an existing Jesse backtest result into Bitcoin AI Lab bridge-format JSON.

The output can be imported at:

```text
https://xonoxo143-ux.github.io/bitcoin-ai-lab/import.html
```

## Safety boundary

The exporter is read-only.

It does not:

- start live trading
- start paper trading
- place orders
- use exchange keys
- modify Jesse simulator behavior
- connect to an exchange

It only reads existing backtest-result data and writes a local JSON file.

## Supported inputs

The exporter supports two input modes.

### 1. Existing Jesse BacktestSession

Use this when Jesse has already run a backtest and saved a BacktestSession.

```bash
python scripts/export_backtest_session_to_lab_json.py \
  --session-id <BACKTEST_SESSION_ID> \
  --output bitcoin_ai_lab_result.json
```

Optional metadata:

```bash
python scripts/export_backtest_session_to_lab_json.py \
  --session-id <BACKTEST_SESSION_ID> \
  --symbol BTC-USDT \
  --timeframe 1h \
  --strategy TrendHunter \
  --bot trend \
  --bot-name "Trend Hunter" \
  --output bitcoin_ai_lab_result.json
```

### 2. Raw saved result JSON

Use this when you already have a JSON file containing Jesse-like result data.

```bash
python scripts/export_backtest_session_to_lab_json.py \
  --input-json raw_jesse_result.json \
  --output bitcoin_ai_lab_result.json
```

This mode is useful for testing the bridge format without needing a configured Jesse database.

## Output format

The output uses Bitcoin AI Lab bridge format:

```json
{
  "version": "bridge-v0.1",
  "engine": "jesse",
  "mode": "backtest",
  "bot": "jesse",
  "botName": "Jesse Backtest",
  "settings": {},
  "summary": {
    "finalValue": 12500,
    "returnPct": 25,
    "maxDrawdownPct": -18.5,
    "trades": 52,
    "fees": 143,
    "slippage": 0,
    "beatHold": null,
    "regime": "Historical",
    "regimeConfidence": "N/A"
  },
  "equity": [],
  "trades": [],
  "replay": [],
  "warnings": []
}
```

The import page mainly uses:

- `summary.finalValue`
- `summary.returnPct`
- `summary.maxDrawdownPct`
- `summary.trades`
- `summary.fees`
- `equity`
- `replay`

## Mapping rules

The exporter maps Jesse fields into lab fields.

```text
Jesse metrics.finishing_balance       → summary.finalValue
Jesse metrics.net_profit_percentage   → summary.returnPct
Jesse metrics.max_drawdown            → summary.maxDrawdownPct
Jesse metrics.total                   → summary.trades
Jesse metrics.fee                     → summary.fees
Jesse equity_curve                    → equity[]
Jesse trades                          → trades[] and replay[]
```

If a field is missing, the exporter should not crash. It adds a warning and sets the missing field to `null` where possible.

## Import flow

After exporting:

1. Open `docs/import.html` through GitHub Pages.
2. Paste the contents of `bitcoin_ai_lab_result.json`.
3. Tap **Import JSON**.
4. Inspect:
   - final value
   - return
   - drawdown
   - trades
   - equity chart
   - replay rows

## Example raw JSON test file

A minimal raw input file can look like this:

```json
{
  "metrics": {
    "starting_balance": 10000,
    "finishing_balance": 12500,
    "net_profit_percentage": 25,
    "max_drawdown": -18.5,
    "total": 52,
    "fee": 143
  },
  "equity_curve": [
    [1672531200000, 10000],
    [1672617600000, 10400],
    [1672704000000, 9800],
    [1672790400000, 11600],
    [1672876800000, 12500]
  ],
  "trades": [
    {
      "side": "long",
      "entry_price": 16750,
      "qty": 0.1,
      "fee": 1.67,
      "PNL": 250
    }
  ]
}
```

Run:

```bash
python scripts/export_backtest_session_to_lab_json.py \
  --input-json sample_raw_result.json \
  --symbol BTC-USDT \
  --timeframe 1h \
  --strategy TrendHunter \
  --bot trend \
  --bot-name "Trend Hunter" \
  --output bitcoin_ai_lab_result.json
```

## Current status

This is the first bridge prototype.

It proves:

```text
Jesse-style result data
→ bridge JSON
→ Bitcoin AI Lab import page
```

It does not yet run a Jesse backtest by itself.

That is intentional. The first stable contract is result conversion, not execution automation.