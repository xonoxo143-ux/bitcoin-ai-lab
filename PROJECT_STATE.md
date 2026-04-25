# Bitcoin AI Lab — Project State

## Current status

This repository is a fork of Jesse. It is still structurally Jesse, but the project identity has now been anchored as Bitcoin AI Lab.

The current visible product is a mobile-first GitHub Pages preview at:

```text
https://xonoxo143-ux.github.io/bitcoin-ai-lab/
```

The bridge/import test page is at:

```text
https://xonoxo143-ux.github.io/bitcoin-ai-lab/import.html
```

The preview runs fully in the browser from `docs/index.html`. It uses fake money and synthetic Bitcoin markets only.

## Core objective

Build a Bitcoin-focused bot lab that can grow into a fully automated trader platform through staged safety gates.

Near term, the platform must:

- run fake-money Bitcoin simulations
- compare bots against baselines
- measure profit and risk
- run batch rankings
- keep replay/debug logs for bot decisions
- persist useful runs locally
- export/import result JSON

Long term, the platform should:

- define strategy personalities
- detect market regimes
- select or weight strategies on the fly
- test adaptive Meta Bot behavior
- bridge into Jesse backtesting/paper trading
- keep real-money execution isolated and disabled by default

## Working philosophy

Start with paper/simulated trading only.

Do not connect this project to real exchange execution until the simulator layer, scoring layer, replay layer, personality layer, regime-detection layer, Meta Bot layer, and bridge layer are trustworthy.

The goal is not to make a magic Bitcoin predictor. The goal is to make bots prove whether their strategy survives different market conditions without cheating, overfitting, or hiding risk.

## What works now

### GitHub Pages mobile preview

Implemented in:

```text
docs/index.html
docs/import.html
```

Current features:

- synthetic BTC market generator
- market scenarios:
  - mixed cycle
  - bull market
  - bear market
  - sideways chop
  - flash crash
- strategy personalities:
  - Adaptive Meta Bot
  - Trend Hunter
  - Risk Turtle
  - HODL Monk
  - Dip Vulture
  - Chaos Monkey
- market regime detector:
  - uptrend
  - downtrend
  - range
  - chop
  - crash
  - recovery
  - unclear
- selected-personality simulation
- batch mode that ranks every personality on the same market
- tournament mode across all markets and multiple seeds
- starting cash input
- seed input
- fee input
- slippage input
- market length input
- volatility input
- random seed button
- final value
- return percentage
- max drawdown
- trade count
- beat-buy-and-hold flag
- verdict label
- BTC/bot/hold chart
- replay table with bot reasons
- local replay persistence via browser storage
- copy/export run JSON
- load saved run
- clear saved run
- import bridge-format result JSON page
- imported-result scoreboard/replay rendering
- Android-readable compact layout

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
+ strategy personality runner
+ fake-money portfolio tracking
+ profit/risk scoreboard
+ batch rankings
+ tournament rankings
+ market regime detector
+ adaptive hard-switch Meta Bot
+ replay/debug logs
+ local persistence
+ result JSON export
+ bridge-format result JSON import page
+ later Jesse bridge
+ much later guarded real exchange integration, if desired
```

## Automated trader platform concept

The fully automated platform should be staged:

```text
1. Static Lab Preview
2. Bot Personality Lab
3. Market Regime Lab
4. Adaptive Meta Bot
5. Result Import/Bridge Contract
6. Jesse Backtest Bridge
7. Paper Trader Platform
8. Guarded Live Trader
```

The Meta Bot is the key future layer. It should watch current/past market conditions, detect the likely market regime, and switch or weight strategy personalities on the fly.

It must not use future candles or hidden scenario labels. No cheating.

## Completed milestones

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

### v0.2 — Batch Rankings

Completed:

- added selected-bot run button
- added batch run button
- runs all current bots on the same generated market
- ranks bots by final value
- highlights winner
- switches chart/replay to selected or winning bot
- lets user tap batch rows to inspect individual bots

### v0.3 — Bot Personalities v1

Completed:

- converted current bots into named strategy personalities
- added trait summaries
- added preferred market and weakness labels
- made batch results read like personality comparisons
- improved replay reasons using personality language

### v0.4 — Market Regime Lab v1

Completed:

- detects trend/chop/crash/recovery from past/current data
- shows regime label during runs
- avoids using future scenario labels in bot decisions
- adds regime notes to result summaries

### v0.5 — Meta Bot v1

Completed:

- added Adaptive Meta Bot
- hard-switches among specialist personalities based on detected regime
- logs switch reasons in replay
- compares Meta Bot against every specialist bot

### v0.6 — Better simulation controls

Completed:

- fee input
- slippage input
- market length input
- volatility input
- random seed button
- export/copy run JSON

### v0.7 — Replay persistence

Completed:

- saved run summaries
- copyable replay JSON
- clearer run metadata
- local browser save/load
- clear saved run

### v0.8 — Jesse bridge planning

Completed:

- added `docs/JESSE_BRIDGE_PLAN.md`
- defined bridge purpose
- defined current browser lab format
- defined desired Jesse capabilities
- defined bridge input/output schema
- identified safe Jesse areas to inspect
- blocked live trading from bridge v1
- defined v0.9 import-result prototype

### v0.9 — Import Result JSON

Completed:

- added `docs/import.html`
- added local-only bridge-format JSON import page
- added sample Jesse-style result JSON
- renders imported scoreboard
- renders imported equity/value chart
- renders imported replay rows
- stores latest imported result locally

## Near-term milestones

### v1.0 — Jesse bridge prototype

- inspect Jesse backtest flow
- identify safe adapter points
- create adapter outside Jesse internals if possible
- export Jesse-style backtest result JSON
- import that result into the browser lab/import page

### v1.1 — Meta Bot v2 / Ensemble Planning

- define weighted strategy allocation
- define conflict handling
- define risk override behavior
- avoid whiplash from rapid rebalancing

## Current cautions

- The package still identifies as `jesse`.
- The repository is large enough that blind renaming is risky.
- We should preserve working Jesse behavior until we know exactly where to hook in.
- This project is educational/simulation-first and should not be represented as financial advice or guaranteed profit software.
- Live trading must remain out of the default user flow.
- Meta Bot strategy switching must not cheat by using future information.
- Jesse bridge v1 is backtest/result-import only.
- No exchange keys should be committed or exposed in GitHub Pages.

## Next best action

Start v1.0 Jesse bridge prototype planning/inspection.

The next concrete move is to inspect Jesse's backtest flow and identify a safe adapter point for exporting bridge-format JSON without touching live trading.