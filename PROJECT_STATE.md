# Bitcoin AI Lab — Project State

## Current status

This repository is a fork of Jesse. At the moment it is still structurally Jesse, not yet a purpose-built Bitcoin AI Lab.

The fork is being repurposed into a simulator/lab where trading bots are tested against Bitcoin market conditions before any real-money behavior is considered.

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

## Initial product shape

Bitcoin AI Lab should become:

```text
Bitcoin AI Lab
= Bitcoin market/backtest engine
+ bot strategy runner
+ paper-money portfolio tracking
+ profit/risk scoreboard
+ replay/debug logs
+ later UI/dashboard
+ much later real exchange integration, if desired
```

## First safe milestone

### v0.1 — Lab Identity Pass

Purpose: make the fork understandable before changing engine behavior.

Tasks:

- add project-state documentation
- add design notes for Bitcoin AI Lab
- identify Jesse files to preserve, wrap, or ignore
- avoid renaming the Python package until the integration risk is understood
- avoid touching live-trading behavior during the first pass

## Near-term milestones

### v0.2 — Bitcoin-only simulation profile

- define a BTC/USD-only default lab mode
- define fake-money starting balance
- define trading fee/slippage defaults
- define baseline strategies:
  - all cash
  - buy and hold
  - random bot
  - simple trend bot

### v0.3 — Bot scoreboard

- final portfolio value
- percent return
- max drawdown
- number of trades
- fees paid
- beat-buy-and-hold flag
- simple verdict label

### v0.4 — Replay logs

- save bot decisions
- save reason strings
- save portfolio state over time
- save comparison to baseline

### v0.5 — Lab UI direction

- decide whether to adapt Jesse's current UI or create a cleaner Bitcoin AI Lab dashboard layer

## Current cautions

- The package still identifies as `jesse`.
- The README still describes Jesse, not Bitcoin AI Lab.
- The repository is large enough that blind renaming is risky.
- We should preserve working Jesse behavior until we know exactly where to hook in.
- This project is educational/simulation-first and should not be represented as financial advice or guaranteed profit software.

## Next best action

Create `docs/BITCOIN_AI_LAB_DESIGN.md` with the first concrete architecture map:

- what Jesse provides
- what Bitcoin AI Lab adds
- which modules are likely touch points
- what v0.1 should change
- what must remain untouched
