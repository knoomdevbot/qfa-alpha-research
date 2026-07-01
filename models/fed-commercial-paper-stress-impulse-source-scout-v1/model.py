"""AR-189 Federal Reserve commercial-paper stress impulse source scout.

This model is intentionally disabled. The source/vintage gate did not pass
because bounded public probes did not prove a complete timestamp-safe first-
vintage commercial-paper outstanding/rate history across the required 2008,
2020, 2022, and recent QT regimes, and the official Fed page states daily CP
posting timing is usual rather than guaranteed.
"""

from __future__ import annotations

MODEL_NAME = "fed-commercial-paper-stress-impulse-source-scout-v1"
ISSUE_ID = "AR-189"

REPRESENTATIVE_SERIES = {
    "COMPOUT": "Commercial Paper Outstanding, all issuers, weekly Wednesday levels",
    "DCPF1M": "1-month AA financial commercial paper rate",
    "DCPF3M": "3-month AA financial commercial paper rate",
    "DCPN3M": "3-month AA nonfinancial commercial paper rate",
}

SOURCE_GATE = {
    "passed": False,
    "reason": (
        "ALFRED vintage snapshots are reachable for some representative CP "
        "series, but the bounded scout did not prove complete first-vintage "
        "mechanics for both outstanding and rates across 2008/2020/2022/recent "
        "regimes; COMPOUT 2008 vintage probing fell back to the current vintage, "
        "and official Fed CP posting time is explicitly not guaranteed."
    ),
}


def generate_signals(context=None):
    """Return a disabled zero-weight signal payload.

    No alpha/performance evaluation was run. The qfa contract is satisfied
    without emitting allocations because AR-189 stopped at the source/vintage
    gate before any Alpaca/qfa market-data evaluation.
    """
    return {
        "weights": {},
        "metadata": {
            "model": MODEL_NAME,
            "issue_id": ISSUE_ID,
            "decision": "rejected_source_gate",
            "source_gate_passed": False,
            "performance_evaluated": False,
            "reason": SOURCE_GATE["reason"],
        },
    }
