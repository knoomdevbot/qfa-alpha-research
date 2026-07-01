"""AR-192 qfa-compatible scaffold for EIA WNGSR storage surprise signals.

The source/vintage gate passed, but the required qfa/Alpaca real ETF
performance run is currently on hold because this execution environment did not
have usable Alpaca credentials.  To avoid deploying an unevaluated alpha, the
wrapper only emits a non-zero allocation when an evaluator provides an explicit,
timestamp-safe WNGSR surprise in the qfa AlphaContext metadata.  Normal daemon
contexts without that metadata receive zero weights.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


DEFAULT_LONG_TIGHT_ETF = "XLE"
DEFAULT_SHORT_LOOSE_ETF = "UNG"
DEFAULT_RISK_CONTROL_ETF = "SHY"
SURPRISE_KEY = "eia_wngsr_storage_surprise_z"
MAX_ABS_WEIGHT = 0.35
MIN_ABS_SURPRISE_Z = 0.75


def _metadata_from_context(context: Any) -> Mapping[str, Any]:
    """Return metadata from qfa AlphaContext-like objects or legacy mappings."""
    if hasattr(context, "metadata"):
        metadata = getattr(context, "metadata")
        if isinstance(metadata, Mapping):
            return metadata
    if isinstance(context, Mapping):
        metadata = context.get("metadata", {})
        if isinstance(metadata, Mapping):
            return metadata
    return {}


def _symbols_from_context(context: Any) -> set[str]:
    """Return available symbols from qfa AlphaContext-like objects or mappings."""
    symbols = getattr(context, "symbols", None)
    if symbols is None and isinstance(context, Mapping):
        symbols = context.get("symbols")
    try:
        return {str(symbol) for symbol in symbols or []}
    except TypeError:
        return set()


def generate_signals(context: Any = None, **kwargs: Any) -> dict[str, float]:
    """Generate compact target weights for a timestamp-safe WNGSR surprise.

    Expected qfa input is an AlphaContext object with ``symbols``, ``prices``,
    ``as_of`` and optional ``metadata``.  A positive surprise means storage was
    tighter than seasonal history (draw/lower build), favoring energy exposure;
    a negative surprise means looser storage, favoring a small UNG short if
    shorting is permitted by the evaluator.  Without an explicit surprise field,
    returns zero weights because AR-192 has not completed its real-data gate.
    """
    _ = kwargs
    metadata = _metadata_from_context(context)
    symbols = _symbols_from_context(context)
    try:
        surprise_z = float(metadata.get(SURPRISE_KEY, 0.0))
    except (TypeError, ValueError):
        surprise_z = 0.0

    if abs(surprise_z) < MIN_ABS_SURPRISE_Z:
        return {}

    scale = min(MAX_ABS_WEIGHT, 0.12 * abs(surprise_z))
    weights: dict[str, float] = {}
    if surprise_z > 0 and DEFAULT_LONG_TIGHT_ETF in symbols:
        weights[DEFAULT_LONG_TIGHT_ETF] = scale
    elif surprise_z < 0 and DEFAULT_SHORT_LOOSE_ETF in symbols:
        weights[DEFAULT_SHORT_LOOSE_ETF] = -scale

    if weights and DEFAULT_RISK_CONTROL_ETF in symbols:
        weights[DEFAULT_RISK_CONTROL_ETF] = 0.0
    return weights
