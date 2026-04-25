# Bitcoin AI Lab Design Notes

## Purpose

Bitcoin AI Lab is a fake-money Bitcoin bot simulator and strategy lab.

The project should make trading bots prove themselves before anything real-money related is considered. A bot should not be judged only by profit. It should also be judged by drawdown, overtrading, fees, consistency, and whether it beats simple baselines.

## Current product shape

The current visible product is the GitHub Pages preview:

```text
https://xonoxo143-ux.github.io/bitcoin-ai-lab/
```

It runs entirely in the browser from `docs/index.html`.

Current preview capabilities:

- synthetic Bitcoin price paths
- fake-money portfolio simulation
- bot selection
- market scenario selection
- starting cash input
- scoreboard
- buy-and-hold comparison
- chart
- replay/debug table

This preview is intentionally small and static. It is the fastest way to test the idea on Android.

## Safety boundary

Default mode is fake-money simulation only.

Do not add live exchange execution until the lab can:

- run repeatable backtests
- compare against baselines
- explain bot decisions
- show drawdown and fees clearly
- save useful replay logs
- block accidental real-money behavior by default

A future real-money unlock should require an explicit config flag and visible warning.

## Relationship to Jesse

This repository is forked from Jesse.

Jesse remains useful as the deeper foundation/reference because it already includes:

- strategy structure
- backtesting
- paper/live trading architecture
- indicators
- metrics
- optimization
- Monte Carlo analysis
- machine-learning hooks
- FastAPI/web app structure

The current mobile preview does not yet call Jesse. That is deliberate. The preview proves the user-facing lab loop first.

## Layer model

```text
Bitcoin AI Lab

1. Static mobile preview
   - docs/index.html
   - runs on GitHub Pages
   - no backend
   - Android-visible immediately
   - synthetic market only

2. Lab model layer
   - bot definitions
   - market scenarios
   - scoring rules
   - replay schema
   - baseline comparisons

3. Jesse bridge layer
   - later integration with Jesse backtests
   - historical candles
   - richer strategy files
   - real metrics
   - optional server mode
```

## Current bots

### Buy & Hold

Buys Bitcoin once at the start and never sells. This is the baseline active bots should try to beat.

### Trend Bot

Uses short and long simple moving averages. It buys when the short trend rises above the long trend and sells when the trend weakens.

### Risk Managed Bot

A cautious trend bot. It caps exposure, buys smaller, and sells faster when weakness appears.

### Dip Buyer

Buys sharp drops and sells sharp spikes. It can perform well in choppy markets but can get hurt in sustained bear markets.

### Random Bot

A deliberately weak baseline. It buys and sells randomly so real strategies have an easy comparison target.

## Current market scenarios

### Mixed Cycle

A synthetic cycle with bull, bear, chop, and recovery phases.

### Bull Market

Positive drift with volatility.

### Bear Market

Negative drift with volatility.

### Sideways Chop

Mean-ish sideways movement with smaller volatility.

### Flash Crash

Normal market behavior interrupted by a sharp crash and later recovery.

## Scoreboard model

Current scoreboard:

- final value
- return percentage
- max drawdown
- trades
- beat buy-and-hold flag
- verdict

Near-term additions:

- fees paid as a visible card
- hold baseline value as a visible card
- exposure level
- win/loss by scenario
- average result across many seeds
- risk-adjusted score

## Replay model

Current replay rows include:

- step
- BTC price
- action
- reason
- portfolio value

This should evolve into a saved run format:

```json
{
  "bot": "trend",
  "market": "mixed",
  "seed": 42,
  "startingCash": 10000,
  "summary": {
    "finalValue": 11420,
    "returnPct": 14.2,
    "maxDrawdownPct": -12.83,
    "trades": 37,
    "beatHold": true
  },
  "steps": []
}
```

## v0.2 target

The next major pass should add better lab controls without touching Jesse internals:

- fee input
- slippage input
- market length input
- volatility slider
- strategy parameter sliders
- run again with random seed
- copy/export run JSON
- compare all bots on the same market

## v0.3 target

Make it a real bot lab instead of a single-run demo:

- multi-seed tournament mode
- bot ranking table
- scenario-by-scenario results
- overtrading penalty
- risk-adjusted score
- saved replay summaries

## v0.4 target

Start Jesse bridge planning:

- identify Jesse's safest backtest entry points
- map Jesse result data to Bitcoin AI Lab's scoreboard
- decide whether the preview remains static or talks to a backend
- keep live trading disabled by default

## Do not do yet

- Do not rename the full Jesse package blindly.
- Do not delete Jesse internals.
- Do not add exchange keys.
- Do not make live trading easy to trigger.
- Do not build an Android APK before the lab loop is stronger.
- Do not overbuild the UI before scoring and replay are useful.

## Current best next move after v0.1 polish

Add compare-all-bots mode.

That is the fastest way to make the lab feel intelligent: one generated market, every bot runs against it, and the app ranks them by profit and risk.