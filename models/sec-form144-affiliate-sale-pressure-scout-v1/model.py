"""SEC Form 144 affiliate-sale pressure scout (source-gate rejected).

The recovery run confirmed limited EDGAR reachability for Form 144 metadata,
but it did not build a durable timestamp-safe parsed event table with
conservative issuer mapping, clustering, breadth/concentration gates, or a
real-data performance evaluator. This model is intentionally disabled and emits
no positions.
"""

MODEL_NAME = "sec-form144-affiliate-sale-pressure-scout-v1"
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
