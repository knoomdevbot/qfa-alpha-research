"""AR-188 ICE/BofA credit-spread first-vintage ETF allocator source scout.

The official ICE/BofA OAS family is not enabled for trading in this model.
The source gate failed because public FRED/ALFRED access showed only a short
2023-07-03+ window for representative investment-grade and high-yield OAS
series, and no durable multi-cycle first-vintage history suitable for
random-window ETF allocation research was proven.
"""

from __future__ import annotations

MODEL_NAME = "ice-bofa-credit-spread-etf-source-scout-v1"
ISSUE_ID = "AR-188"

REPRESENTATIVE_SERIES = {
    "BAMLH0A0HYM2": "ICE BofA US High Yield Index Option-Adjusted Spread",
    "BAMLC0A0CM": "ICE BofA US Corporate Index Option-Adjusted Spread",
    "BAMLC0A4CBBB": "ICE BofA BBB US Corporate Index Option-Adjusted Spread",
    "BAMLH0A1HYBB": "ICE BofA BB US High Yield Index Option-Adjusted Spread",
}

SOURCE_GATE = {
    "passed": False,
    "reason": (
        "Public FRED/ALFRED pages and graph CSVs for representative ICE/BofA "
        "OAS series expose only roughly three years of public observations "
        "starting 2023-07-03 and do not prove durable timestamp-safe first-"
        "vintage coverage across multiple credit cycles."
    ),
}


def generate_signals(context=None):
    """Return a disabled zero-weight signal payload.

    The qfa contract is intentionally satisfied without placing orders or
    emitting allocations because AR-188 stopped at the source/vintage gate.
    """
    return {
        "weights": {},
        "metadata": {
            "model": MODEL_NAME,
            "issue_id": ISSUE_ID,
            "decision": "rejected_source_gate",
            "source_gate_passed": False,
            "reason": SOURCE_GATE["reason"],
        },
    }
