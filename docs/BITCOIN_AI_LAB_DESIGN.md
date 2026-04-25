# Bitcoin AI Lab Design Notes

## Purpose

Bitcoin AI Lab is a fake-money Bitcoin bot simulator, strategy lab, and staged foundation for a fully automated trader platform.

The project should make trading bots prove themselves before anything real-money related is considered. A bot should not be judged only by profit. It should also be judged by drawdown, overtrading, fees, consistency, and whether it beats simple baselines.

Long term, the platform should be able to detect what kind of market it appears to be in, choose the best strategy personality for that moment, and switch or weight strategies on the fly. That adaptive layer is called the Meta Bot.

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
- batch rankings for all current bots on the same market

This preview is intentionally small and static. It is the fastest way to test the idea on Android.

## Safety boundary

Default mode is fake-money simulation only.

Do not add live exchange execution until the lab can:

- run repeatable backtests
- compare against baselines
- explain bot decisions
- show drawdown and fees clearly
- save useful replay logs
- test many market regimes
- prove adaptive strategy switching without future knowledge
- block accidental real-money behavior by default

A future real-money unlock should require an explicit config flag, visible warning, and separate execution layer.

## Fully automated trader platform direction

Bitcoin AI Lab should grow in stages:

```text
Stage 1: Static Lab Preview
- fake money
- synthetic markets
- simple bots
- batch rankings
- Android-visible through GitHub Pages

Stage 2: Bot Personality Lab
- named trader archetypes
- trait-weighted decision logic
- strengths and weaknesses
- market preference profiles

Stage 3: Market Regime Lab
- detect trend, chop, crash, recovery, volatility spikes
- score what the market appears to be doing using only past/current data
- run scenario-specific tournaments

Stage 4: Meta Bot
- chooses or weights bot personalities based on current regime
- switches strategy on the fly
- logs why it switched
- must not use future information

Stage 5: Paper Trader Platform
- real historical candles
- paper/live data feed without real orders
- persistent run logs
- dashboard and alerts

Stage 6: Guarded Live Trader
- optional and disabled by default
- explicit real-money unlock
- strict max loss, max position, and emergency stop controls
- exchange connector isolated from lab logic
```

The current product is Stage 1. The next strategic target is Stage 2 and Stage 3, because those make the later Meta Bot meaningful.

## Strategy personality model

Bots should evolve from one-off hardcoded scripts into trader personalities.

A personality should be a data object with decision traits:

```text
Bot Personality
- id
- name
- role
- description
- aggression
- patience
- trend bias
- dip bias
- risk tolerance
- take-profit bias
- panic sensitivity
- conviction scaling
- overtrade tendency
- max exposure
- preferred market regimes
- known weaknesses
```

The same market signal can produce different actions depending on personality. For example:

- a trend hunter buys momentum
- a dip buyer buys fear
- a risk turtle waits or cuts exposure
- a profit sniper exits sooner
- a crash survivor moves toward cash

The replay should explain decisions using the bot's personality, not generic action text.

## Meta Bot model

The Meta Bot is the platform's adaptive trader.

It should not trade from one fixed personality. It should decide which strategy personality, or mix of personalities, is best for the current market.

The Meta Bot can use:

- recent trend strength
- recent volatility
- drawdown from recent peak
- recovery strength
- chop/noise level
- current exposure
- recent bot performance using past data only
- regime confidence

The Meta Bot cannot use:

- future candles
- future winning bot results
- post-run knowledge
- hidden scenario labels during a live/paper run

### Hard switching

Simple version:

```text
If market looks like strong uptrend -> use Trend Hunter
If market looks like sharp dip -> use Dip Buyer
If market looks like crash -> use Crash Survivor
If market looks like chop -> use Profit Sniper or Risk Turtle
```

### Weighted strategy allocation

Better version:

```text
Trend Hunter: 50%
Risk Turtle: 30%
Dip Buyer: 20%
```

The Meta Bot adjusts weights as market conditions change. This avoids whiplash from switching too often.

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
   - batch rankings

3. Personality layer
   - trait-weighted bots
   - named archetypes
   - strengths and weaknesses
   - bot explanations

4. Regime detection layer
   - trend/chop/crash/recovery detection
   - volatility scoring
   - regime confidence
   - no future knowledge

5. Meta Bot layer
   - strategy switching
   - strategy weighting
   - switch cooldowns
   - adaptive risk control
   - switch replay explanations

6. Jesse bridge layer
   - later integration with Jesse backtests
   - historical candles
   - richer strategy files
   - real metrics
   - optional server mode

7. Execution guard layer
   - paper/live separation
   - explicit live unlock
   - position limits
   - loss limits
   - emergency stop
   - exchange connector isolation
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

## Future bot personalities

### Trend Hunter

Momentum specialist. Likes confirmed uptrends and lets winners run.

### Dip Vulture

Buys sharp drops when it thinks panic is overdone.

### Risk Turtle

Prioritizes survival, low drawdown, and smaller exposure.

### Profit Sniper

Takes smaller gains quickly and avoids overstaying trades.

### Crash Survivor

Cuts exposure fast when volatility and drawdown spike.

### Accumulator

Slowly builds BTC over time instead of making big all-in moves.

### Chaos Monkey

Random/stress-test bot used as a weak baseline.

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
- batch ranking

Near-term additions:

- fees paid as a visible card
- hold baseline value as a visible card
- exposure level
- win/loss by scenario
- average result across many seeds
- risk-adjusted score
- best bot per regime
- Meta Bot switch count
- Meta Bot regime accuracy

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
  "regimes": [],
  "switches": [],
  "steps": []
}
```

For Meta Bot runs, replay should also include:

- detected regime
- confidence
- active strategy or strategy weights
- switch reason
- cooldown status
- risk override status

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

Add Bot Personalities v1:

- convert current bots into named archetypes
- add trait summaries
- add preferred market and weakness labels
- make batch results read like personality comparisons

## v0.5 target

Add Market Regime Lab v1:

- detect trend/chop/crash/recovery from past/current data
- show regime label during runs
- rank best bots by regime
- avoid using future scenario labels in bot decisions

## v0.6 target

Add Meta Bot v1:

- strategy switching or weighting
- cooldown to avoid whiplash
- switch replay explanations
- compare Meta Bot against every specialist bot

## v0.7 target

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
- Do not let the Meta Bot cheat by looking ahead.

## Current best next move

Add Bot Personalities v1, then Market Regime Lab v1.

That is the clean path toward a fully automated trader platform because strategy switching only matters once the platform understands both bot personalities and market regimes.