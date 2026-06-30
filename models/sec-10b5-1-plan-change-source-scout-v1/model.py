"""SEC 10b5-1 plan-change source scout (source-gate rejected).

A bounded SEC Item 408 / Rule 10b5-1 disclosure probe did not establish a
sufficient timestamp-safe, liquid, mapped event table. This wrapper is
intentionally inert and emits no positions.
"""

MODEL_NAME = "sec-10b5-1-plan-change-source-scout-v1"
MODEL_STATUS = "rejected_source_gate"


def generate_signals(context):
    """Return zero target weights for all supported context shapes.

    The source/event-table gate failed before any market-data performance run,
    so the context is intentionally unused.
    """

    return {}
