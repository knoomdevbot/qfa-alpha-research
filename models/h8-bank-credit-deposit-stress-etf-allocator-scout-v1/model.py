"""AR-160 H.8 bank credit/deposit stress ETF allocator scout.

Real qfa/Alpaca evaluation completed; artifact decision is rejection/watchlist in
evaluations/latest.json. The model remains disabled and emits zero weights unless
manually re-enabled by a future approved refinement.
"""

MODEL_NAME = "h8-bank-credit-deposit-stress-etf-allocator-scout-v1"
MODEL_STATUS = "disabled_after_realdata_evaluation"

def generate_signals(context):
    """qfa-compatible disabled signal: return no target weights."""
    return {}
