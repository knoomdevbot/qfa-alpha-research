"""Zero-weight scaffold for AR-171 SEC 8-K Item 2.02 event-table scout.

The bounded source gate passed, but no timestamp-safe post-filing return
performance evaluator has been run. This model intentionally emits no weights
until a durable event parser, historical common-stock mapping, and real-data
performance evaluation are added.
"""

MODEL_NAME = "sec-8k-item202-accepted-filing-event-table-scout-v1"


def generate_signals(context):
    """Return no target weights; scaffold only, no orders or daemon usage."""
    return {}
