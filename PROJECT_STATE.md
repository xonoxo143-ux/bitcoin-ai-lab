# Bitcoin AI Lab — Project State

## Current status

This repository is a fork of Jesse. It is still structurally Jesse, but the project identity has now been anchored as Bitcoin AI Lab.

The current visible product is a mobile-first GitHub Pages preview at:

```text
https://xonoxo143-ux.github.io/bitcoin-ai-lab/
```

The preview runs fully in the browser from `docs/index.html`. It uses fake money and synthetic Bitcoin markets only.

## Core objective

Build a Bitcoin-focused bot lab that can:

- run fake-money Bitcoin simulations
- compare bots against baselines
- measure profit and risk
- keep replay/debug logs for bot decisions
- eventually use Jesse's backtesting, metrics, optimization, Monte Carlo, and machine-learning features where useful

## Working philosophy

Start with paper/simulated trading only.

Do not connect this project to real exchange execution until the simulator layer, scoring layer, and replay layer are trustworthy.

The goal is not to make a magic Bitcoin predictor. The goal is to make bots prove whether their strategy survives different market conditions without cheating, overfitting, or hiding risk.

## What works now

### GitHub Pages mobile preview

Implemented in:

```text
docs/index.html
```

Current features:

- synthetic BTC market generator
- market scenarios:
  - mixed cycle
  - bull market
  - bear market
  - sideways chop
  - flash crash
- bot choices:
  - trend bot
  - risk managed bot
  - buy and hold
  - dip buyer
  - random bot
- starting cash input
- seed input
- final value
- return percentage
- max drawdown
- trade count
- beat-buy-and-hold flag
- verdict label
- BTC/bot/hold chart
- replay table with bot reasons
- Android-readable layout

## Why Jesse is the base

Jesse already provides useful trading-framework machinery:

- strategy definitions
- backtesting
- paper/live trading architecture
- technical indicators
- metrics
- optimization
- Monte Carlo testing
- machine-learning hooks
- FastAPI/web app structure

For Bitcoin AI Lab, the most useful pieces are the strategy, backtest, metrics, Monte Carlo, and ML systems. The live-trading pieces should stay secondary until much later.

## Current product shape

```text
Bitcoin AI Lab
= mobile browser preview
+ synthetic Bitcoin market simulator
+ bot strategy runner
+ fake-money portfolio tracking
+ profit/risk scoreboard
+ replay/debug logs
+ later Jesse bridge
+ much later real exchange integration, if desired
```

## Completed milestone

### v0.1 — Mobile Shell Polish

Completed:

- updated README for Bitcoin AI Lab identity
- improved `docs/index.html` mobile preview
- added bot explanation text
- added risk managed bot
- added buy-and-hold comparison
- added verdict label
- improved chart legend/readability
- improved replay table with decision reasons
- added `docs/BITCOIN_AI_LAB_DESIGN.md`

## Near-term milestones

### v0.2 — Better simulation controls

- fee input
- slippage input
- market length input
- volatility slider
- strategy parameter sliders
- random seed button
- export/copy run JSON

### v0.3 — Compare-all-bots mode

- run all bots on the same market
- rank by final value
- rank by risk-adjusted score
- show which bot beat buy-and-hold
- show scenario-by-scenario results

### v0.4 — Replay persistence

- saved run summaries
- downloadable/copyable replay JSON
- clearer run metadata
- import/replay by seed and settings

### v0.5 — Jesse bridge planning

- identify safe Jesse backtest entry points
- map Jesse backtest outputs into the Bitcoin AI Lab scoreboard
- keep live trading disabled by default

## Current cautions

- The package still identifies as `jesse`.
- The repository is large enough that blind renaming is risky.
- We should preserve working Jesse behavior until we know exactly where to hook in.
- This project is educational/simulation-first and should not be represented as financial advice or guaranteed profit software.
- Live trading must remain out of the default user flow.

## Next best action

Add compare-all-bots mode to the GitHub Pages preview.

This is the fastest next improvement because it turns the preview from a single-run demo into an actual lab: one market, multiple bots, ranked results.