"""AR-175 Federal Reserve SLOOS source-gate rejected scaffold.

The scout did not prove official timestamp-safe historical release dates/times
and immutable first-vintage SLOOS component values from dated Federal Reserve
pages. This research-only model therefore emits zero weights and must not be
used for allocation.
"""

CANDIDATE_POOL = (
    "XLF",
    "KRE",
    "HYG",
    "LQD",
    "IWM",
    "SPY",
    "XLP",
    "TLT",
    "IEF",
)


def generate_signals(context):
    """Return zero target weights after source/vintage-gate rejection."""
    return {symbol: 0.0 for symbol in CANDIDATE_POOL}
