"""SEC Form 4 insider imbalance source scout (source-gate rejected).

A bounded recovery probe confirmed SEC submissions metadata reachability,
acceptance timestamps, and parseable raw Form 4 XML for a small sample. It did
not build the required durable 2018-2026 timestamp-safe mapped clustered event
table or any real-data performance evaluator. This model is intentionally
zero-weight and emits no positions.
"""

MODEL_NAME = "sec-form4-insider-imbalance-source-scout-v1"
MODEL_STATUS = "rejected_source_gate"


def generate_signals(context):
    """Return zero target weights for all supported context shapes.

    The source/event-table gate failed before any alpha or performance claim was
    validated, so the context is intentionally unused.
    """

    return {}
