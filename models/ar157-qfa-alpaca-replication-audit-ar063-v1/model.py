"""AR-186 qfa/Alpaca-only replication audit of AR-063 macro-drawdown ETF allocator.

Rule-based, deterministic validator model; not optimized or intended for live use.
"""
from __future__ import annotations

from typing import Any


def generate_signals(context: Any) -> dict[str, float]:
    """Return simple deterministic weights for qfa contract smoke tests.

    The durable evaluation reconstructs the frozen macro-drawdown allocator with
    vectorized qfa/Alpaca daily bars in the run artifact. This wrapper is kept
    side-effect-free and contains no data access, orders, or optimization. It
    accepts both qfa AlphaContext objects and dict-like smoke-test contexts.
    """
    if isinstance(context, dict):
        symbols = context.get("symbols") or []
    else:
        symbols = getattr(context, "symbols", []) or []
    if not symbols:
        return {}
    weight = 1.0 / min(len(symbols), 10)
    return {symbol: weight for symbol in symbols[:10]}
