"""Federal Reserve G.19 consumer-credit impulse ETF source scout.

Bounded source-vintage micro-scout only. The official Fed G.19 release archive
is reachable, but no durable cross-vintage parser, event table, or market-data
performance evaluator was built in this recovery pass. This model is therefore
intentionally inert and emits no target weights.
"""

MODEL_NAME = "fed-g19-consumer-credit-impulse-etf-scout-v1"
MODEL_STATUS = "rejected_source_gate_recovery_micro_scout"


def generate_signals(context):
    """Return zero target weights for all supported context shapes."""

    return {}
