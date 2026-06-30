"""SEC 13F holdings-change crowding/uncrowding scout (source-gate rejected).

A bounded EDGAR probe confirmed 13F-HR information-table reachability,
acceptance timestamps, and same-filer quarter-to-quarter CUSIP change mechanics.
The research did not establish a conservative, timestamp-safe CUSIP-to-ticker /
common-stock mapping with liquid daily-bar coverage, so no performance alpha was
validated. This model is intentionally disabled and emits no positions.
"""

MODEL_NAME = "sec-13f-holdings-change-crowding-scout-v1"
MODEL_STATUS = "rejected_source_gate"


def generate_signals(context):
    """Return zero target weights for all supported context shapes.

    Parameters
    ----------
    context : object
        qfa-style context or a plain mapping. It is intentionally unused because
        the source/mapping gate failed before any tradable alpha was validated.

    Returns
    -------
    dict
        Empty target-weight mapping; the strategy is disabled.
    """

    return {}
