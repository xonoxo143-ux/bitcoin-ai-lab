# Bitcoin AI Lab — Project State

## Current status

This repository is a fork of Jesse. It is still structurally Jesse, but the project identity has now been anchored as Bitcoin AI Lab.

The current visible product is a mobile-first GitHub Pages preview at:

```text
https://xonoxo143-ux.github.io/bitcoin-ai-lab/
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

Long term, the platform should:

- define strategy personalities
- detect market regimes
- select or weight strategies on the fly
- test adaptive Meta Bot behavior
- bridge into Jesse backtesting/paper trading
- keep real-money execution isolated and disabled by default

## Working philosophy

Start with paper/simulated trading only.

Do not connect this project to real exchange execution until the simulator layer, scoring layer, replay layer, personality layer, regime-detection layer, and Meta Bot layer are trustworthy.

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
- selected-bot simulation
- batch mode that ranks every bot on the same market
- final value
- return percentage
- max drawdown
- trade count
- beat-buy-and-hold flag
- verdict label
- BTC/bot/hold chart
- replay table with bot reasons
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
+ bot strategy runner
+ fake-money portfolio tracking
+ profit/risk scoreboard
+ batch rankings
+ replay/debug logs
+ later bot personality layer
+ later market regime detector
+ later adaptive Meta Bot
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
5. Paper Trader Platform
6. Guarded Live Trader
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

## Near-term milestones

### v0.3 — Bot Personalities v1

- convert current bots into named strategy personalities
- add trait summaries
- add preferred market and weakness labels
- make batch results read like personality comparisons
- improve replay reasons using personality language

### v0.4 — Market Regime Lab v1

- detect trend/chop/crash/recovery from past/current data
- show regime label during runs
- rank best bots by regime
- avoid using future scenario labels in bot decisions

### v0.5 — Meta Bot v1

- add adaptive strategy switching or weighting
- add cooldown to avoid whiplash
- add switch replay explanations
- compare Meta Bot against every specialist bot

### v0.6 — Better simulation controls

- fee input
- slippage input
- market length input
- volatility slider
- strategy parameter sliders
- random seed button
- export/copy run JSON

### v0.7 — Replay persistence

- saved run summaries
- downloadable/copyable replay JSON
- clearer run metadata
- import/replay by seed and settings

### v0.8 — Jesse bridge planning

- identify safe Jesse backtest entry points
- map Jesse backtest outputs into the Bitcoin AI Lab scoreboard
- keep live trading disabled by default

## Current cautions

- The package still identifies as `jesse`.
- The repository is large enough that blind renaming is risky.
- We should preserve working Jesse behavior until we know exactly where to hook in.
- This project is educational/simulation-first and should not be represented as financial advice or guaranteed profit software.
- Live trading must remain out of the default user flow.
- Meta Bot strategy switching must not cheat by using future information.

## Next best action

Add Bot Personalities v1.

This is now the most important next layer because adaptive automation only works if the platform knows what each strategy is good at and what kind of market it prefers.