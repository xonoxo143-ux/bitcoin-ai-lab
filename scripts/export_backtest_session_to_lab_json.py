#!/usr/bin/env python3
"""
Export a Jesse backtest result into Bitcoin AI Lab bridge-format JSON.

This script is intentionally read-only. It does not start paper trading, live trading,
or exchange execution. It only reads an existing BacktestSession or a raw result JSON
file and writes a bridge-format JSON file that can be imported at:

    docs/import.html

Typical usage from a Jesse project environment:

    python scripts/export_backtest_session_to_lab_json.py \
        --session-id <BACKTEST_SESSION_ID> \
        --output bitcoin_ai_lab_result.json

Fallback usage with a raw JSON file:

    python scripts/export_backtest_session_to_lab_json.py \
        --input-json raw_jesse_result.json \
        --output bitcoin_ai_lab_result.json
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

BRIDGE_VERSION = "bridge-v0.1"
DEFAULT_OUTPUT = "bitcoin_ai_lab_result.json"


class BridgeExportError(RuntimeError):
    """Raised when the bridge exporter cannot safely produce a result."""


def safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if value is None:
            return default
        if isinstance(value, str) and value.strip() == "":
            return default
        n = float(value)
        if math.isnan(n) or math.isinf(n):
            return default
        return n
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    n = safe_float(value, None)
    if n is None:
        return default
    return int(n)


def first_present(mapping: Dict[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return default


def timestamp_to_iso(value: Any) -> Any:
    """Convert millisecond/second timestamps to ISO strings when obvious."""
    n = safe_float(value, None)
    if n is None:
        return value

    # Jesse commonly stores ms timestamps. Some exports may use seconds.
    if n > 10_000_000_000:
        seconds = n / 1000
    else:
        seconds = n

    try:
        return datetime.fromtimestamp(seconds, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except (OverflowError, OSError, ValueError):
        return value


def normalize_equity_curve(equity_curve: Any) -> List[Dict[str, Any]]:
    """
    Normalize Jesse equity curve variants into:
        [{"time": ..., "value": ...}, ...]

    Accepts common forms:
    - [{"time": ..., "value": ...}, ...]
    - [{"timestamp": ..., "balance": ...}, ...]
    - [[time, value], ...]
    - [10000, 10050, ...]
    """
    if not equity_curve:
        return []

    normalized: List[Dict[str, Any]] = []

    for idx, item in enumerate(equity_curve):
        time_value: Any = idx
        equity_value: Optional[float] = None

        if isinstance(item, dict):
            time_value = first_present(
                item,
                ["time", "timestamp", "date", "created_at", "t"],
                idx,
            )
            equity_value = safe_float(
                first_present(
                    item,
                    ["value", "equity", "balance", "portfolio_value", "portfolioValue", "y"],
                ),
                None,
            )
        elif isinstance(item, (list, tuple)):
            if len(item) >= 2:
                time_value = item[0]
                equity_value = safe_float(item[1], None)
            elif len(item) == 1:
                equity_value = safe_float(item[0], None)
        else:
            equity_value = safe_float(item, None)

        if equity_value is None:
            continue

        normalized.append({
            "time": timestamp_to_iso(time_value),
            "value": equity_value,
        })

    return normalized


def infer_trade_side(trade: Dict[str, Any]) -> str:
    raw = str(first_present(trade, ["side", "type", "position_type", "direction"], "trade")).lower()

    if "long" in raw or "buy" in raw:
        return "buy"
    if "short" in raw or "sell" in raw:
        return "sell"
    return raw.upper() if raw else "TRADE"


def infer_trade_price(trade: Dict[str, Any]) -> Optional[float]:
    direct = safe_float(
        first_present(
            trade,
            [
                "price",
                "entry_price",
                "entry",
                "exit_price",
                "exit",
                "average_price",
                "avg_price",
            ],
        ),
        None,
    )
    if direct is not None:
        return direct

    orders = trade.get("orders")
    if isinstance(orders, list) and orders:
        for order in orders:
            if isinstance(order, dict):
                order_price = safe_float(first_present(order, ["price", "executed_price", "avg_price"]), None)
                if order_price is not None:
                    return order_price

    return None


def normalize_trades(trades: Any) -> List[Dict[str, Any]]:
    if not trades:
        return []

    normalized: List[Dict[str, Any]] = []
    for idx, raw_trade in enumerate(trades):
        if not isinstance(raw_trade, dict):
            continue

        side = infer_trade_side(raw_trade)
        price = infer_trade_price(raw_trade)
        qty = safe_float(first_present(raw_trade, ["qty", "quantity", "size", "contracts"]), None)
        fee = safe_float(first_present(raw_trade, ["fee", "fees", "commission"]), 0.0)
        pnl = safe_float(first_present(raw_trade, ["PNL", "pnl", "profit", "net_profit"]), None)
        time_value = first_present(
            raw_trade,
            ["opened_at", "closed_at", "time", "timestamp", "created_at", "updated_at"],
            idx,
        )

        normalized.append({
            "time": timestamp_to_iso(time_value),
            "side": side,
            "price": price,
            "qty": qty,
            "fee": fee,
            "pnl": pnl,
            "reason": f"Jesse {side} trade",
            "raw": raw_trade,
        })

    return normalized


def build_replay_rows(
    trades: List[Dict[str, Any]],
    equity: List[Dict[str, Any]],
) -> List[List[Any]]:
    rows: List[List[Any]] = []

    for idx, trade in enumerate(trades):
        value = None
        if idx < len(equity):
            value = equity[idx].get("value")
        elif equity:
            value = equity[-1].get("value")

        rows.append([
            idx + 1,
            trade.get("price"),
            str(trade.get("side", "TRADE")).upper(),
            trade.get("reason") or "Jesse trade",
            value,
        ])

    if not rows and equity:
        for idx, point in enumerate(equity[:250]):
            rows.append([
                idx + 1,
                None,
                "EQUITY",
                "Jesse equity curve point",
                point.get("value"),
            ])

    return rows


def estimate_final_value(metrics: Dict[str, Any], equity: List[Dict[str, Any]]) -> Optional[float]:
    direct = safe_float(
        first_present(
            metrics,
            ["finishing_balance", "final_value", "finalValue", "ending_balance", "current_balance"],
        ),
        None,
    )
    if direct is not None:
        return direct
    if equity:
        return safe_float(equity[-1].get("value"), None)
    return None


def estimate_return_pct(metrics: Dict[str, Any], final_value: Optional[float]) -> Optional[float]:
    direct = safe_float(
        first_present(metrics, ["net_profit_percentage", "returnPct", "return_pct", "return"]),
        None,
    )
    if direct is not None:
        return direct

    starting_balance = safe_float(first_present(metrics, ["starting_balance", "start", "startingBalance"]), None)
    if starting_balance and final_value is not None:
        return ((final_value - starting_balance) / starting_balance) * 100
    return None


def build_bridge_result(
    *,
    metrics: Dict[str, Any],
    equity_curve: Any,
    trades: Any,
    settings: Optional[Dict[str, Any]] = None,
    source: str = "unknown",
    bot: str = "jesse",
    bot_name: str = "Jesse Backtest",
    session_id: Optional[str] = None,
    warnings: Optional[List[str]] = None,
) -> Dict[str, Any]:
    settings = settings or {}
    warnings = warnings or []

    equity = normalize_equity_curve(equity_curve)
    normalized_trades = normalize_trades(trades)
    final_value = estimate_final_value(metrics, equity)
    return_pct = estimate_return_pct(metrics, final_value)
    max_drawdown = safe_float(first_present(metrics, ["max_drawdown", "maxDrawdownPct", "drawdown"]), None)
    trade_count = safe_int(first_present(metrics, ["total", "trades", "trade_count", "tradeCount"], len(normalized_trades)))
    fees = safe_float(first_present(metrics, ["fee", "fees", "commission"], 0.0), 0.0)

    if final_value is None:
        warnings.append("Could not determine final value from metrics or equity curve.")
    if return_pct is None:
        warnings.append("Could not determine return percentage from metrics.")
    if max_drawdown is None:
        warnings.append("Could not determine max drawdown from metrics.")

    bridge = {
        "version": BRIDGE_VERSION,
        "engine": "jesse",
        "mode": "backtest",
        "source": source,
        "sessionId": session_id,
        "bot": bot,
        "botName": bot_name,
        "settings": settings,
        "summary": {
            "finalValue": final_value,
            "returnPct": return_pct,
            "maxDrawdownPct": max_drawdown,
            "trades": trade_count,
            "fees": fees,
            "slippage": safe_float(first_present(metrics, ["slippage", "slip"], 0.0), 0.0),
            "beatHold": None,
            "regime": "Historical",
            "regimeConfidence": "N/A",
            "winRate": safe_float(first_present(metrics, ["win_rate", "winRate"], None), None),
            "sharpeRatio": safe_float(first_present(metrics, ["sharpe_ratio", "sharpeRatio"], None), None),
            "sortinoRatio": safe_float(first_present(metrics, ["sortino_ratio", "sortinoRatio"], None), None),
        },
        "equity": equity,
        "trades": normalized_trades,
        "replay": build_replay_rows(normalized_trades, equity),
        "warnings": warnings,
    }

    return bridge


def load_raw_result_json(path: Path) -> Tuple[Dict[str, Any], Any, Any, Dict[str, Any], List[str]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    warnings: List[str] = []

    # Already bridge-shaped. Normalize through the exporter anyway when possible.
    metrics = data.get("metrics") or data.get("summary") or data
    equity = data.get("equity_curve") or data.get("equity") or []
    trades = data.get("trades") or []
    settings = data.get("settings") or {}

    if "summary" in data and "metrics" not in data:
        warnings.append("Input looked bridge-shaped; used summary as metrics source.")

    return metrics, equity, trades, settings, warnings


def load_backtest_session(session_id: str) -> Tuple[Dict[str, Any], Any, Any, Dict[str, Any], List[str]]:
    try:
        from jesse.models.BacktestSession import get_backtest_session_by_id
    except Exception as exc:  # pragma: no cover - depends on Jesse environment
        raise BridgeExportError(
            "Could not import Jesse BacktestSession model. Run this from a configured Jesse environment "
            "or use --input-json instead."
        ) from exc

    session = get_backtest_session_by_id(session_id)
    if session is None:
        raise BridgeExportError(f"BacktestSession not found: {session_id}")

    warnings: List[str] = []
    if getattr(session, "status", None) != "finished":
        warnings.append(f"BacktestSession status is {getattr(session, 'status', None)!r}, not 'finished'.")

    settings = {
        "sessionId": str(session_id),
        "createdAt": timestamp_to_iso(getattr(session, "created_at", None)),
        "updatedAt": timestamp_to_iso(getattr(session, "updated_at", None)),
        "executionDuration": getattr(session, "execution_duration", None),
    }

    return (
        session.metrics_json or {},
        session.equity_curve_json or [],
        session.trades_json or [],
        settings,
        warnings,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Jesse backtest results to Bitcoin AI Lab JSON.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--session-id", help="Existing Jesse BacktestSession id to export.")
    source.add_argument("--input-json", type=Path, help="Raw Jesse result JSON file to convert.")

    parser.add_argument("--output", type=Path, default=Path(DEFAULT_OUTPUT), help="Output bridge JSON path.")
    parser.add_argument("--bot", default="jesse", help="Lab bot id to write into the result.")
    parser.add_argument("--bot-name", default="Jesse Backtest", help="Display name for the imported result.")
    parser.add_argument("--symbol", help="Optional symbol override, e.g. BTC-USDT.")
    parser.add_argument("--timeframe", help="Optional timeframe override, e.g. 1h.")
    parser.add_argument("--strategy", help="Optional strategy name override.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.session_id:
        metrics, equity, trades, settings, warnings = load_backtest_session(args.session_id)
        source = "BacktestSession"
        session_id = args.session_id
    else:
        metrics, equity, trades, settings, warnings = load_raw_result_json(args.input_json)
        source = str(args.input_json)
        session_id = None

    if args.symbol:
        settings["symbol"] = args.symbol
    if args.timeframe:
        settings["timeframe"] = args.timeframe
    if args.strategy:
        settings["strategy"] = args.strategy

    bridge = build_bridge_result(
        metrics=metrics or {},
        equity_curve=equity or [],
        trades=trades or [],
        settings=settings,
        source=source,
        bot=args.bot,
        bot_name=args.bot_name,
        session_id=session_id,
        warnings=warnings,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(bridge, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote Bitcoin AI Lab bridge JSON: {args.output}")
    if bridge["warnings"]:
        print("Warnings:")
        for warning in bridge["warnings"]:
            print(f"- {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
