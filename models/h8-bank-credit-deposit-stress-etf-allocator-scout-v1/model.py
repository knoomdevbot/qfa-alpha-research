"""H.8 bank credit/deposit stress ETF allocator scout scaffold.

Source/vintage feasibility passed in bounded recovery, but no qfa/Alpaca
real-market-data performance evaluation was run. This scaffold is deliberately
disabled and emits no target weights until a durable real-data evaluator is
completed.
"""

MODEL_NAME = "h8-bank-credit-deposit-stress-etf-allocator-scout-v1"
MODEL_STATUS = "source_gate_passed_needs_realdata_evaluation"


def generate_signals(context):
    """Return zero target weights for all supported context shapes.

    The context is intentionally unused because AR-160 has only passed the
    timestamp/source gate; alpha efficacy has not been validated.
    """

    return {}
