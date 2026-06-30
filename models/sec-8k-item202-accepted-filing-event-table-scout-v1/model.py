"""Zero-weight rejected scaffold for AR-171 SEC 8-K Item 2.02 event scout.

The source/event-table gate was feasible, but the timestamp-safe qfa/Alpaca
real-data performance evaluator failed the predeclared cost/control gate. This
model intentionally emits no weights and is disabled.
"""

MODEL_NAME = "sec-8k-item202-accepted-filing-event-table-scout-v1"


def generate_signals(context):
    """Return no target weights; rejected scaffold only, no orders or daemon usage."""
    return {}
