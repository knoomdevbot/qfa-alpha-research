"""SEC common-stock offering/prospectus acceptance feasibility scout.

AR-153 is intentionally inert. The bounded recovery run did not build a
conservative timestamp-safe liquid common-stock offering event table, so no
trading signal is enabled.
"""


def generate_signals(context):
    """Return zero weights for the rejected source-gate scout."""
    _ = context
    return {}
