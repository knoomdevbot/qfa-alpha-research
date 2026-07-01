"""AR-192 disabled source-gate scaffold for EIA WNGSR storage vintages.

This wrapper intentionally emits zero weights. Source/vintage feasibility passed
for compact official archived storage-table samples, but no market-data
performance evaluation has been run.
"""

from __future__ import annotations

from typing import Any


def generate_signals(data: Any = None, **kwargs: Any) -> dict[str, float]:
    """Return zero target weights until a real-data evaluation is approved."""
    _ = (data, kwargs)
    return {}
