"""AR-191 SEC 8-K Item 1.01/2.01 source-gate rejection scaffold.

The hard-capped SEC metadata scout did not produce a durable, class-separated,
conservatively mapped event table. This model intentionally emits no tradable
signals.
"""


def generate_signals(context):
    """Return zero weights/no signals for the rejected source-gate scout."""
    return {}
