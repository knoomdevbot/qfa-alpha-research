"""Disabled AR-190 Treasury auction-result demand-share ETF scout.

The official-source gate passed, but the real qfa/Alpaca daily ETF performance
evaluation failed robustness/acceptance gates after next-session execution and
turnover costs. Keep the model zero-weight and inactive.
"""

MODEL_NAME = "treasury-auction-result-demand-share-source-scout-v1"
ENABLED = False
WEIGHT = 0.0

def generate_signals(context):
    """Return no weights for rejected research artifact; never places orders."""
    return {}
