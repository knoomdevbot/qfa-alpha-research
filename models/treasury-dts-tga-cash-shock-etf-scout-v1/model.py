"""AR-170 Treasury DTS/TGA source-gate scaffold.

The official FiscalData Daily Treasury Statement tables are reachable, but this
scout rejects the alpha before performance evaluation because the API rows do
not expose an immutable vintage/publication timestamp sufficient to prove the
record_date-to-publication_date convention required by the issue.  To avoid
lookahead in live/replay contexts this model intentionally emits zero weights.
"""

from __future__ import annotations


def generate_signals(context) -> dict[str, float]:
    """Return zero target weights for all requested symbols.

    The source/vintage gate failed; no tradable DTS/TGA allocator is enabled.
    """
    return {symbol: 0.0 for symbol in list(getattr(context, "symbols", []))}
