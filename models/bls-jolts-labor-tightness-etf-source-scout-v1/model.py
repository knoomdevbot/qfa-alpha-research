"""Zero-weight scaffold for AR-173 JOLTS source/vintage scout.

The source/vintage gate failed, so this model intentionally emits no
positions. Do not use current revised JOLTS values for historical signals.
"""


def generate_signals(context):
    """Return an empty/zero allocation until timestamp-safe vintages exist.

    Parameters
    ----------
    context : object
        Optional runtime context supplied by an evaluator.

    Returns
    -------
    dict
        Empty weights plus rejection metadata. The shape is deliberately simple
        and side-effect free for downstream smoke tests.
    """
    return {
        "weights": {},
        "metadata": {
            "model": "bls-jolts-labor-tightness-etf-source-scout-v1",
            "decision": "rejected_source_gate",
            "reason": "official BLS release-date pages blocked and no unauthenticated multi-vintage JOLTS values verified",
        },
    }
