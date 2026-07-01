"""AR-179 SEC buyback authorization source-gate rejection scaffold.

The bounded official SEC EDGAR micro-scout did not produce a durable,
timestamp-safe broad event table, so this model emits no tradable signals.
"""


def generate_signals(context):
    """Return no signals for the rejected source-gate scout."""
    return {}
