"""AR-180 FDA approval-decision source-gate rejection scaffold.

The bounded official FDA Drugs@FDA scout did not prove timestamp-safe
next-session public availability for a broad official event table, so this
model emits no tradable signals.
"""


def generate_signals(context):
    """Return no signals for the rejected source-gate scout."""
    return {}
