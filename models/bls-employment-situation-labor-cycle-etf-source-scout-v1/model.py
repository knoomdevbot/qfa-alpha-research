"""AR-174 source-gate rejected scaffold.

The required official BLS Employment Situation release-calendar/archive proof was
not reproducibly available in the scout run, so this model intentionally emits
zero weights and must not be used for live allocation.
"""

CANDIDATE_POOL = (
    "XLY", "XLI", "IWM", "QQQ", "XLP", "XLU", "XLV", "SPY",
    "TLT", "IEF", "HYG", "LQD", "GLD", "DBC",
)


def generate_signals(context):
    """Return a zero-weight scaffold after source/vintage-gate rejection."""
    return {symbol: 0.0 for symbol in CANDIDATE_POOL}
