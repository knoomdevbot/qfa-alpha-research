"""Zero-weight scaffold for AR-158 Reg SHO threshold-list source feasibility scout.

This model intentionally emits no tradable positions.  The source gate found official
Reg SHO threshold-list endpoints but did not complete a full timestamp-safe,
liquid-mapped event table and no real daily-bar performance evaluation was run.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Dict, Iterable, List, Optional, Tuple
import re


@dataclass(frozen=True)
class ThresholdRow:
    symbol: str
    security_name: str
    market_category: str
    threshold_flag: str


TRAILER_RE = re.compile(r"^\d{14}$")


def parse_threshold_text(text: str) -> Tuple[List[ThresholdRow], Optional[str]]:
    """Parse official pipe-delimited threshold-list text.

    Supports Nasdaq Trader `nasdaqthYYYYMMDD.txt` and NYSE regulatory download
    files.  Returns only rows with Reg SHO Threshold Flag == 'Y' plus the
    exchange timestamp trailer when present.
    """
    lines = [line.strip() for line in text.replace("\r", "").split("\n") if line.strip()]
    if not lines or not lines[0].startswith("Symbol|"):
        raise ValueError("not a recognized Reg SHO threshold-list file")
    rows: List[ThresholdRow] = []
    trailer: Optional[str] = None
    for line in lines[1:]:
        if TRAILER_RE.fullmatch(line):
            trailer = line
            continue
        parts = line.split("|")
        if len(parts) >= 4 and parts[0].strip() and parts[3].strip().upper() == "Y":
            rows.append(
                ThresholdRow(
                    symbol=parts[0].strip().upper(),
                    security_name=parts[1].strip(),
                    market_category=parts[2].strip(),
                    threshold_flag=parts[3].strip().upper(),
                )
            )
    return rows, trailer


def classify_state(prev_symbols: Iterable[str], cur_symbols: Iterable[str]) -> Dict[str, List[str]]:
    """Return sampled add/remove/persist symbol sets for two dated files."""
    prev = set(prev_symbols)
    cur = set(cur_symbols)
    return {
        "adds": sorted(cur.difference(prev)),
        "removes": sorted(prev.difference(cur)),
        "persists": sorted(cur.intersection(prev)),
    }


def content_fingerprint(content: bytes) -> str:
    """Compact reproducibility fingerprint for source probes."""
    return sha256(content).hexdigest()[:16]


def generate_signals(context):
    """Return an empty signal map; AR-158 is rejected at source-gate stage."""
    return {}
