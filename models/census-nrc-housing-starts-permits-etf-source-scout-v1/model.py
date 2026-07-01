"""AR-183 Census/HUD New Residential Construction source/vintage scout.

This is a disabled, zero-weight qfa wrapper plus reusable source parser helpers.
The source gate passed for feasibility only: official Census archive documents
carry release timestamps and first-published headline permits/starts/completions.
A later market-data performance evaluation rejected the allocator; generate_signals
continues to emit no positions.
"""

from __future__ import annotations

import io
import re
from dataclasses import dataclass

from typing import Dict, Iterable, Optional

try:
    import requests
except Exception:  # pragma: no cover - runtime dependency in source scout only
    requests = None

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - optional for qfa import smoke tests
    PdfReader = None

ARCHIVE_URL = "https://www.census.gov/construction/nrc/data/releases.html"
USER_AGENT = "Mozilla/5.0 AR-183 census-nrc-source-scout/1.0"


@dataclass(frozen=True)
class NRCEvent:
    """Timestamp-safe event parsed from an official Census/HUD release."""

    release_month: str
    release_date_text: str
    release_time_text: str
    source_url: str
    permits_saar_thousands: Optional[int]
    starts_saar_thousands: Optional[int]
    completions_saar_thousands: Optional[int]
    prior_permits_revised_thousands: Optional[int] = None
    prior_starts_revised_thousands: Optional[int] = None
    prior_completions_revised_thousands: Optional[int] = None


def _normalize(text: str) -> str:
    return (
        text.replace("\xa0", " ")
        .replace("‐", "-")
        .replace("–", "-")
        .replace("—", "-")
        .replace("\u2011", "-")
    )


def _int_thousands(match: Optional[re.Match]) -> Optional[int]:
    if not match:
        return None
    return int(match.group(1).replace(",", ""))


def discover_archive_links(html_text: str) -> Dict[str, list[str]]:
    """Return official NRC PDF/TXT release links embedded in the archive page."""
    text = html_text.replace("\\/", "/")
    pdfs = sorted(
        set(
            re.findall(
                r"https://www[.]census[.]gov/construction/nrc/pdf/newresconst_[0-9]{6}[.]pdf",
                text,
            )
        )
    )
    txts = sorted(
        set(
            re.findall(
                r"https://www[.]census[.]gov/construction/nrc/txt/c(?:20|22)_[0-9]{4}[.]txt",
                text,
            )
        )
    )
    return {"pdf": pdfs, "txt": txts}


def pdf_bytes_to_text(content: bytes, max_pages: int = 2) -> str:
    """Extract text from an official NRC PDF without writing raw data to disk."""
    if PdfReader is None:
        raise RuntimeError("pypdf is required for PDF extraction")
    reader = PdfReader(io.BytesIO(content))
    return "\n".join(page.extract_text() or "" for page in reader.pages[:max_pages])


def parse_release_text(text: str, source_url: str, release_month: str = "") -> NRCEvent:
    """Parse headline first-published values from a Census/HUD NRC release.

    Supports the modern unified New Residential Construction PDF layout and the
    legacy text layout used around 1995-2001. Values are SAAR thousands. The
    parser intentionally returns None for fields not present in a source file
    rather than imputing from current/revised tables.
    """
    t = _normalize(text)
    compact = re.sub(r"\s+", " ", t)

    date_text = "not_found"
    time_text = "not_found"
    m = re.search(
        r"FOR RELEASE AT\s+([0-9:]+\s*[AP][.]?M[.]?\s*[A-Z]{3}),\s*([A-Z]+,\s+[A-Z]+\s+\d{1,2},\s+\d{4})",
        compact,
        re.I,
    )
    if m:
        time_text = m.group(1).replace(".", "")
        date_text = m.group(2).title()
    else:
        m = re.search(
            r"For Release\s+([0-9:]+\s*[AP][.]?M[.]?\s*[A-Z]{3}),\s*([A-Za-z]+,\s+[A-Za-z]+\s+\d{1,2},\s+\d{4})",
            compact,
        )
        if m:
            time_text = m.group(1).replace(".", "")
            date_text = m.group(2)

    block_match = re.search(
        r"NEW RESIDENTIAL\s+CONSTRUCTION.*?(?:Next Release|Seasonally Adjusted)",
        compact,
        re.I,
    )
    block = block_match.group(0) if block_match else compact[:2500]

    permits = _int_thousands(re.search(r"Building Permits:?\s*([0-9,]+),000", block, re.I))
    starts = _int_thousands(re.search(r"Housing Starts:?\s*([0-9,]+),000", block, re.I))
    completions = _int_thousands(re.search(r"Housing Completions:?\s*([0-9,]+),000", block, re.I))

    # Legacy c20 text releases: starts/permits are narrative sections.
    if starts is None:
        starts = _int_thousands(
            re.search(r"housing starts .*? seasonally adjusted annual rate of\s+([0-9,]+),000", compact, re.I)
        )
    if permits is None:
        permits = _int_thousands(
            re.search(r"housing units authorized by building\s+permits .*? was\s+([0-9,]+),000", compact, re.I)
        )
    # Legacy c22 text releases: completions only.
    if completions is None:
        completions = _int_thousands(
            re.search(r"housing completions .*? seasonally\s+adjusted annual rate of\s+([0-9,]+),000", compact, re.I)
        )

    prior_permits = _int_thousands(
        re.search(r"Building Permits.*?revised\s+\w+\s+(?:rate|figure).*?of\s+([0-9,]+),000", compact, re.I)
    )
    prior_starts = _int_thousands(
        re.search(r"Housing Starts.*?revised\s+\w+\s+estimate\s+of\s+([0-9,]+),000", compact, re.I)
    )
    prior_completions = _int_thousands(
        re.search(r"Housing Completions.*?revised\s+\w+\s+(?:estimate|rate)\s+of\s+([0-9,]+),000", compact, re.I)
    )

    return NRCEvent(
        release_month=release_month,
        release_date_text=date_text,
        release_time_text=time_text,
        source_url=source_url,
        permits_saar_thousands=permits,
        starts_saar_thousands=starts,
        completions_saar_thousands=completions,
        prior_permits_revised_thousands=prior_permits,
        prior_starts_revised_thousands=prior_starts,
        prior_completions_revised_thousands=prior_completions,
    )


def fetch_official_event(url: str, timeout: int = 30) -> NRCEvent:
    """Fetch and parse one official Census/HUD NRC release URL in memory."""
    if requests is None:
        raise RuntimeError("requests is required for source fetching")
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    response.raise_for_status()
    release_month = ""
    m = re.search(r"(?:newresconst_|c(?:20|22)_)([0-9]{4,6})", url)
    if m:
        release_month = m.group(1)
    if url.lower().endswith(".pdf"):
        text = pdf_bytes_to_text(response.content)
    else:
        text = response.text
    return parse_release_text(text, source_url=url, release_month=release_month)


def build_event_table(urls: Iterable[str], limit: Optional[int] = None) -> list[NRCEvent]:
    """Build a timestamp-safe event table from official release URLs.

    This helper is bounded by caller-supplied URL lists and does not persist raw
    downloads. It is intended for future real-data evaluation after independent
    review fixes timing conventions and ETF coverage.
    """
    out = []
    for i, url in enumerate(urls):
        if limit is not None and i >= limit:
            break
        out.append(fetch_official_event(url))
    return out


def generate_signals(context=None):
    """Disabled zero-weight qfa wrapper: no orders, no market-data claims."""
    return {
        "weights": {},
        "metadata": {
            "model": "census-nrc-housing-starts-permits-etf-source-scout-v1",
            "decision": "rejected_realdata_disabled_scaffold",
            "reason": "official Census/HUD source gate passed; real-data ETF allocator failed robustness/control gates",
        },
    }
