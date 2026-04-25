# Bitcoin AI Lab

Bitcoin AI Lab is a fake-money Bitcoin bot simulator and strategy lab.

The current public preview runs directly in the browser through GitHub Pages:

```text
https://xonoxo143-ux.github.io/bitcoin-ai-lab/
```

## Current status

This repository is a fork of Jesse. It is being repurposed into Bitcoin AI Lab.

Right now, the visible product is a static mobile-first browser preview in `docs/index.html`. It does not connect to an exchange, does not place real trades, and does not use real money.

The original Jesse codebase remains in place as the deeper trading-framework foundation/reference for later backtesting, strategy, metrics, optimization, Monte Carlo, machine-learning, and possible paper-trading integration.

## What works now

The GitHub Pages preview currently includes:

- synthetic Bitcoin market generation
- selectable market scenarios: mixed, bull, bear, chop, crash
- selectable bots: trend bot, buy and hold, dip buyer, random bot
- fake starting cash
- trading fee simulation
- final value
- return percentage
- max drawdown
- trade count
- buy-and-hold comparison
- simple risk verdict
- chart
- replay/debug table

## What this is not

Bitcoin AI Lab is not financial advice.

Bitcoin AI Lab is not a guaranteed-profit system.

Bitcoin AI Lab is not currently a live trading app.

The near-term goal is to make strategies prove themselves in fake-money simulations before anything real is even considered.

## Project direction

The project has two layers:

```text
1. Mobile preview layer
   - GitHub Pages
   - static HTML/CSS/JS
   - fast Android testing
   - fake-money simulations

2. Jesse foundation layer
   - Python trading framework
   - backtesting
   - paper/live architecture
   - indicators
   - metrics
   - optimization
   - Monte Carlo
   - machine learning
```

The mobile preview lets the idea be tested quickly on Android. Jesse remains the serious engine/reference for later.

## Near-term roadmap

### v0.1 — Mobile shell polish

- improve Android readability
- improve chart and replay visibility
- explain bot behavior
- add buy-and-hold comparison
- add risk verdict
- clarify repo identity

### v0.2 — Better simulation controls

- starting balance input
- fee/slippage controls
- market length controls
- more market scenarios
- saved run summaries

### v0.3 — Stronger bot lab

- more baseline bots
- strategy parameter sliders
- multi-seed tournaments
- bot rankings
- richer replay logs

### v0.4 — Jesse bridge planning

- identify the safest hooks into Jesse
- map Jesse backtest outputs into the lab scoreboard
- decide whether the preview stays static or talks to a backend

## Repository map

```text
docs/index.html                 Mobile GitHub Pages preview
docs/BITCOIN_AI_LAB_DESIGN.md   Project design notes
PROJECT_STATE.md                Current project state and milestones
jesse/                          Original Jesse framework code
```

## Jesse attribution

This project is forked from Jesse, an MIT-licensed crypto trading framework for researching, backtesting, optimizing, and trading strategies.

Original project:

```text
https://github.com/jesse-ai/jesse
```

The fork keeps Jesse intact while Bitcoin AI Lab is developed around it.