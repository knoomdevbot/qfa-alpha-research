"""Zero-weight source-gate rejection scaffold for AR-172.

AR-172 asked whether official exchange-reported, bi-monthly short-interest
publication records could support a timestamp-safe broad common-stock event
table.  The bounded scout did not find a reproducible free/public historical
source with both broad listed-security records and official publication dates.
No performance evaluation was run.
"""

MODEL_NAME = "exchange-reported-short-interest-publication-scout-v1"


def generate_signals(context):
    """Return no target weights; rejected source-gate scaffold only."""
    return {}
