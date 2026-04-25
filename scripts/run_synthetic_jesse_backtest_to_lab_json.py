#!/usr/bin/env python3
"""
Run minimal Jesse backtests against synthetic BTC candles and export the result
into Bitcoin AI Lab bridge-format JSON.

This proves the bridge path:

    synthetic 1m candles
    -> Jesse backtest simulator
    -> Bitcoin AI Lab bridge JSON
    -> docs/import.html

Safety boundary:
- no exchange keys
- no paper trading
- no live trading
- no network candle import
- no real orders

This script uses Jesse's actual backtest simulator with in-memory synthetic candles.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Type

import numpy as np

# Force Jesse down its test/silent path. This avoids dashboard multiprocessing,
# Redis status loops, and BacktestSession database writes.
os.environ.setdefault("PYTEST_CURRENT_TEST", "bitcoin-ai-lab-synthetic-backtest")

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from jesse.config import config
from jesse.enums import exchanges
from jesse.routes import router
from jesse.services.validators import validate_routes
from jesse.services import order_service, position_service, exchange_service
from jesse.store import store
from jesse.strategies import Strategy
from jesse.modes.backtest_mode import simulator

from scripts.export_backtest_session_to_lab_json import build_bridge_result


class SyntheticTimedHold(Strategy):
    """Base class for safe bridge-proof strategies.

    These strategies only open one long position and hold. That keeps this proof
    focused on Jesse engine execution and bridge export instead of complicated
    Strategy API behavior.
    """

    ENTRY_INDEX = 30
    POSITION_SIZE = 0.05
    LAB_BOT = "jesse-synthetic-timed-hold"
    LAB_BOT_NAME = "Jesse Synthetic Timed Hold"

    def should_long(self) -> bool:
        return self.index == self.ENTRY_INDEX and self.position.is_close

    def go_long(self) -> None:
        self.buy = (self.POSITION_SIZE, self.price)

    def should_short(self) -> bool:
        return False


class SyntheticEarlyHold(SyntheticTimedHold):
    ENTRY_INDEX = 30
    POSITION_SIZE = 0.05
    LAB_BOT = "jesse-synthetic-early-hold"
    LAB_BOT_NAME = "Jesse Early Hold"


class SyntheticMidHold(SyntheticTimedHold):
    ENTRY_INDEX = 240
    POSITION_SIZE = 0.05
    LAB_BOT = "jesse-synthetic-mid-hold"
    LAB_BOT_NAME = "Jesse Mid Hold"


class SyntheticLateHold(SyntheticTimedHold):
    ENTRY_INDEX = 480
    POSITION_SIZE = 0.05
    LAB_BOT = "jesse-synthetic-late-hold"
    LAB_BOT_NAME = "Jesse Late Hold"


class SyntheticBoldEarlyHold(SyntheticTimedHold):
    ENTRY_INDEX = 30
    POSITION_SIZE = 0.12
    LAB_BOT = "jesse-synthetic-bold-early-hold"
    LAB_BOT_NAME = "Jesse Bold Early Hold"


STRATEGIES: List[Type[SyntheticTimedHold]] = [
    SyntheticEarlyHold,
    SyntheticMidHold,
    SyntheticLateHold,
    SyntheticBoldEarlyHold,
]


def make_synthetic_candles(seed: int, count: int, start_price: float) -> np.ndarray:
    rng = np.random.default_rng(seed)
    timestamp = 1_672_531_200_000  # 2023-01-01T00:00:00Z
    price = start_price
    rows: List[List[float]] = []

    for i in range(count):
        if i < count * 0.35:
            drift = 0.0009
        elif i < count * 0.55:
            drift = -0.0014
        elif i < count * 0.78:
            drift = math.sin(i / 11) * 0.0007
        else:
            drift = 0.0011

        noise = rng.normal(0, 0.006)
        old = price
        close = max(1000.0, old * (1 + drift + noise))
        high = max(old, close) * (1 + abs(rng.normal(0, 0.0025)))
        low = min(old, close) * (1 - abs(rng.normal(0, 0.0025)))
        volume = max(1.0, 100 + rng.normal(0, 12))

        # Jesse candle shape is [timestamp, open, close, high, low, volume].
        rows.append([timestamp, old, close, high, low, volume])
        timestamp += 60_000
        price = close

    return np.array(rows, dtype=float)


def configure_jesse(
    exchange: str,
    symbol: str,
    timeframe: str,
    starting_balance: float,
    fee: float,
    strategy_cls: Type[SyntheticTimedHold],
) -> None:
    config["app"]["trading_mode"] = "backtest"
    config["app"]["debug_mode"] = False
    config["env"]["data"]["warmup_candles_num"] = 0
    config["env"]["exchanges"][exchange] = {
        "fee": fee,
        "type": "futures",
        "futures_leverage": 1,
        "futures_leverage_mode": "cross",
        "balance": starting_balance,
    }

    routes = [{
        "exchange": exchange,
        "symbol": symbol,
        "timeframe": timeframe,
        "strategy": strategy_cls,
    }]

    router.initiate(routes, data_routes=[])
    store.reset()
    store.app.set_session_id(f"bitcoin-ai-lab-{strategy_cls.LAB_BOT}")
    validate_routes(router)
    store.candles.init_storage(5000)
    exchange_service.initialize_exchanges_state()
    order_service.initialize_orders_state()
    position_service.initialize_positions_state()


def run_one_strategy(args: argparse.Namespace, strategy_cls: Type[SyntheticTimedHold]) -> Dict:
    exchange = exchanges.SANDBOX
    symbol = "BTC-USDT"
    timeframe = "1m"

    configure_jesse(exchange, symbol, timeframe, args.starting_balance, args.fee, strategy_cls)

    candles = make_synthetic_candles(args.seed, args.candles, args.start_price)
    key = f"{exchange}-{symbol}"
    candles_payload = {
        key: {
            "exchange": exchange,
            "symbol": symbol,
            "candles": candles,
        }
    }

    result = simulator(
        candles_payload,
        run_silently=True,
        generate_equity_curve=True,
        generate_hyperparameters=True,
        # Keep benchmark disabled. Benchmark output queries the candle DB, but this
        # runner intentionally uses in-memory synthetic candles and no database import.
        benchmark=False,
        fast_mode=False,
    )

    return build_bridge_result(
        metrics=result.get("metrics") or {},
        equity_curve=result.get("equity_curve") or [],
        trades=result.get("trades") or [],
        settings={
            "exchange": exchange,
            "symbol": symbol,
            "timeframe": timeframe,
            "strategy": strategy_cls.__name__,
            "startingBalance": args.starting_balance,
            "fee": args.fee,
            "candles": args.candles,
            "seed": args.seed,
            "source": "synthetic-in-memory-candles",
            "entryIndex": strategy_cls.ENTRY_INDEX,
            "positionSize": strategy_cls.POSITION_SIZE,
        },
        source="synthetic_jesse_backtest",
        bot=strategy_cls.LAB_BOT,
        bot_name=strategy_cls.LAB_BOT_NAME,
        warnings=[
            "Synthetic candle data. This proves Jesse engine integration, not market realism.",
            "Timed hold strategies are intentionally simple. Strategy quality is not the target of this bridge proof.",
            "Benchmark output is disabled because the synthetic runner does not import candles into Jesse's database."
        ],
    )


def run_backtests(args: argparse.Namespace) -> Dict:
    results = [run_one_strategy(args, strategy_cls) for strategy_cls in STRATEGIES]
    ranked = sorted(
        results,
        key=lambda item: float(item.get("summary", {}).get("finalValue") or 0),
        reverse=True,
    )
    winner = deepcopy(ranked[0])

    return {
        "version": "bridge-v0.2",
        "engine": "jesse",
        "mode": "backtest-comparison",
        "source": "synthetic_jesse_backtest_comparison",
        "sessionId": None,
        "bot": winner.get("bot"),
        "botName": winner.get("botName"),
        "settings": {
            "symbol": "BTC-USDT",
            "timeframe": "1m",
            "startingBalance": args.starting_balance,
            "fee": args.fee,
            "candles": args.candles,
            "seed": args.seed,
            "startPrice": args.start_price,
            "strategyCount": len(results),
            "source": "synthetic-in-memory-candles",
        },
        "summary": winner.get("summary", {}),
        "equity": winner.get("equity", []),
        "replay": winner.get("replay", []),
        "ranking": [
            {
                "rank": i + 1,
                "bot": item.get("bot"),
                "botName": item.get("botName"),
                "summary": item.get("summary", {}),
                "settings": item.get("settings", {}),
            }
            for i, item in enumerate(ranked)
        ],
        "results": ranked,
        "warnings": [
            "Synthetic comparison data. This proves multi-strategy Jesse bridge integration, not market realism.",
            "All included strategies are simple timed long entries; they are bridge probes, not trading recommendations.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run synthetic Jesse backtests and export Bitcoin AI Lab JSON.")
    parser.add_argument("--output", type=Path, default=Path("bitcoin_ai_lab_synthetic_jesse_result.json"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--candles", type=int, default=720, help="Number of synthetic 1m candles.")
    parser.add_argument("--start-price", type=float, default=70_000)
    parser.add_argument("--starting-balance", type=float, default=10_000)
    parser.add_argument("--fee", type=float, default=0.001, help="Trading fee as decimal. 0.001 = 0.1%")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bridge = run_backtests(args)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bridge, indent=2), encoding="utf-8")
    print(f"Wrote synthetic Jesse bridge comparison result: {args.output}")
    print("Import it at docs/import.html or the GitHub Pages import URL.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
