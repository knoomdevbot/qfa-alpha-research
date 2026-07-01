"""AR-176 source-gate rejection scaffold.

The official BEA Personal Income and Outlays vintage-source gate did not
clear, so this model intentionally emits no tradable weights.
"""


def generate_signals(context):
    """Return a zero-weight signal dictionary for the provided context.

    Parameters
    ----------
    context : object
        Unused runtime context supplied by the evaluator.

    Returns
    -------
    dict
        Empty weights and metadata documenting source-gate rejection.
    """
    return {
        "weights": {},
        "metadata": {
            "model": "bea-personal-income-outlays-consumer-impulse-source-scout-v1",
            "status": "rejected_source_gate",
            "reason": "official dated BEA pages are reachable, but bounded parser proof was incomplete across older and recent vintages",
        },
    }
