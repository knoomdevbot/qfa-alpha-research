"""SEC N-PORT holdings-change pressure scout (source-gate rejected).

The research run did not build a conservative timestamp-safe holdings-change
event table with reliable public ticker/CUSIP mapping and liquid-bar coverage.
This model is intentionally disabled and emits no positions.
"""

MODEL_NAME = "sec-nport-holdings-change-pressure-scout-v1"
MODEL_STATUS = "rejected_source_gate"


def generate_signals(context):
    """Return zero target weights for all supported context shapes.

    Parameters
    ----------
    context : object
        qfa-style context or a plain mapping. It is intentionally unused because
        the source gate failed before any performance alpha was validated.

    Returns
    -------
    dict
        Empty target-weight mapping; the strategy is disabled.
    """

    return {}
