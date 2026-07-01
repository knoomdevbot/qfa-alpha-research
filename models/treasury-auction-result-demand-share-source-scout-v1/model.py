"""Disabled source-gate scaffold for AR-190 Treasury auction result demand-share scout."""

MODEL_NAME = "treasury-auction-result-demand-share-source-scout-v1"
ENABLED = False
WEIGHT = 0.0

def generate_signals(context):
    """Return zero weights until source-gate pass is followed by real-data evaluation."""
    return {}
