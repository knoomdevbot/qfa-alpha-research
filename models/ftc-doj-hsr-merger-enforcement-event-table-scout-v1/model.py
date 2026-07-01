"""AR-181 FTC/DOJ HSR merger-enforcement source-gate rejection scaffold.

The official-source scout did not produce a durable, timestamp-safe,
conservatively mapped liquid U.S. common-stock event table, so this model
emits no tradable signals.
"""


def generate_signals(context):
    """Return zero weights/no signals for the rejected source-gate scout."""
    return {}
