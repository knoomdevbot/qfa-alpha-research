"""FINRA margin-debt leverage-cycle ETF allocator scout.

Research status: rejected after bounded fast-falsification.  The source was
reachable and a conservative publication lag was applied, but the post-cost
allocator failed to dominate static/trend and inverted/shifted controls.  This
module is intentionally disabled for production use and emits no positions.
"""

MODEL_NAME = "finra-margin-debt-leverage-cycle-etf-scout-v1"
MODEL_STATUS = "rejected_fast_falsification"
SELECTED_UNIVERSE = [
    "SPY",
    "QQQ",
    "IWM",
    "HYG",
    "LQD",
    "TLT",
    "IEF",
    "SHY",
    "GLD",
    "UUP",
    "DBC",
    "XLP",
    "XLU",
    "XLV",
    "XLF",
    "XLK",
]


def generate_signals(context):
    """Return target weights for the qfa-style context.

    The scout was rejected and must not place trades, so no targets are emitted.
    The unused ``context`` argument is accepted for compatibility with the alpha
    model interface.
    """

    return {}
