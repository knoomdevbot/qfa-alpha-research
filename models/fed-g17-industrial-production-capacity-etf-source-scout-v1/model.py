"""Federal Reserve G.17 source/vintage scout zero-weight qfa wrapper.

This module intentionally contains no trading signal.  It provides a small,
timestamp-safe parser for official Federal Reserve G.17 dated release text pages
so a later real-data evaluator can build first-vintage event tables without
using current-revised macro data or market CSVs.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime
from html import unescape
import re
from typing import Iterable, Optional
from urllib.parse import urljoin

try:  # requests is optional at import time for qfa wrappers.
    import requests
except Exception:  # pragma: no cover
    requests = None

BASE_URL = "https://www.federalreserve.gov/releases/g17/"
RELEASE_DATES_URL = urljoin(BASE_URL, "release_dates.htm")
USER_AGENT = "qfa-alpha-research AR-182 G17 source scout (no orders)"


@dataclass(frozen=True)
class G17FirstVintageEvent:
    release_date: str
    release_time_et: str
    release_timezone_label: str
    observation_month: str
    official_text_url: str
    indpro_total_index: float
    indpro_total_mom_pct: float
    capacity_utilization_total: float
    capacity_utilization_total_change_pp: Optional[float]
    manufacturing_index: Optional[float]
    manufacturing_mom_pct: Optional[float]
    manufacturing_capacity_utilization: Optional[float]


def zero_weights(symbols: Iterable[str]) -> dict[str, float]:
    """Return an explicitly disabled/zero allocation for qfa scaffolding."""
    return {str(symbol): 0.0 for symbol in symbols}


def generate_signals(context) -> dict[str, float]:
    """qfa alpha contract: disabled source-gate scaffold returns zero weights."""
    return zero_weights(getattr(context, "symbols", []))


def fetch_url(url: str, timeout: int = 15) -> str:
    if requests is None:  # pragma: no cover
        raise RuntimeError("requests is required for live source parsing")
    response = requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
    return response.text


def parse_release_dates_html(html: str) -> list[dict[str, str]]:
    """Parse official release_dates.htm preformatted month -> release date rows."""
    match = re.search(r"<pre[^>]*>(.*?)</pre>", html, flags=re.I | re.S)
    if not match:
        raise ValueError("official G.17 release_dates.htm <pre> block not found")
    text = unescape(match.group(1))
    month_re = re.compile(
        r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
        r"(\d{4})\s+(\d{1,2})-([A-Za-z]+)-(\d{4})\s*$"
    )
    rows: list[dict[str, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        m = month_re.match(line)
        if not m:
            continue
        obs_month_name, obs_year, rel_day, rel_month_name, rel_year = m.groups()
        rel_dt = datetime.strptime(f"{rel_day}-{rel_month_name}-{rel_year}", "%d-%B-%Y").date()
        obs_dt = datetime.strptime(f"1-{obs_month_name}-{obs_year}", "%d-%B-%Y").date()
        rows.append({"observation_month": obs_dt.isoformat()[:7], "release_date": rel_dt.isoformat()})
    if not rows:
        raise ValueError("no release date rows parsed from official G.17 page")
    return rows


def list_archive_text_links(index_html: str, start_yyyymmdd: str = "20010201") -> list[str]:
    """Return dated official g17.txt links, excluding benchmark revision folders."""
    links = []
    for href in re.findall(r"href=[\"']([^\"']+g17\.txt)[\"']", index_html, flags=re.I):
        cleaned = href.strip().lstrip("./")
        match = re.match(r"^(\d{8})/g17\.txt$", cleaned, flags=re.I)
        if not match:
            continue
        if match.group(1) < start_yyyymmdd:
            continue
        full = urljoin(BASE_URL, cleaned)
        links.append(full)
    return sorted(set(links))


def _numbers_from_bar_line(line: str) -> list[float]:
    values = []
    for token in re.findall(r"(?<![A-Za-z])[-+]?\d*\.?\d+", line.replace("--", " ")):
        values.append(float(token))
    return values


def _last_month_header(header_line: str) -> str:
    # Example: "... Oct.[r]    Nov.[p]".  Return the final month name.
    names = re.findall(r"(Jan\.?|Feb\.?|Mar\.?|Apr\.?|May|June|July|Aug\.?|Sept\.?|Sep\.?|Oct\.?|Nov\.?|Dec\.?)\s*(?:\[[rp]\])?", header_line)
    if not names:
        raise ValueError("no month labels found in G.17 table header")
    norm = {"Jan.": "Jan", "Feb.": "Feb", "Mar.": "Mar", "Apr.": "Apr", "Aug.": "Aug", "Sept.": "Sep", "Sep.": "Sep", "Oct.": "Oct", "Nov.": "Nov", "Dec.": "Dec"}
    final_name = names[-1]
    return norm.get(final_name, final_name)


def _parse_table_row(lines: list[str], start_idx: int, row_name: str) -> tuple[Optional[float], Optional[float]]:
    for line in lines[start_idx : start_idx + 80]:
        if line.strip().lower().startswith(row_name.lower()):
            parts = line.split("|")
            if len(parts) < 3:
                return None, None
            left_nums = _numbers_from_bar_line(parts[1])
            mid_nums = _numbers_from_bar_line(parts[2])
            return (left_nums[-1] if left_nums else None, mid_nums[-1] if mid_nums else None)
    return None, None


def _parse_capacity_row(lines: list[str], start_idx: int, row_name: str) -> Optional[float]:
    """Parse the latest capacity-utilization rate from the monthly panel."""
    for line in lines[start_idx : start_idx + 80]:
        if line.strip().lower().startswith(row_name.lower()):
            parts = line.split("|")
            if len(parts) < 3:
                return None
            monthly_nums = _numbers_from_bar_line(parts[2])
            return monthly_nums[-1] if monthly_nums else None
    return None


def parse_g17_release_text(text: str, url: str) -> G17FirstVintageEvent:
    """Parse a dated official g17.txt into a compact first-vintage event."""
    lines = text.splitlines()
    release_line = next((ln for ln in lines[:20] if "For release at" in ln), "")
    release_date_line = next((ln for ln in lines[:25] if re.search(r"\b\w+ \d{1,2}, \d{4}\b", ln)), "")
    dm = re.search(r"\b([A-Za-z]+ \d{1,2}, \d{4})\b", release_date_line)
    if not dm:
        raise ValueError("release date line not found")
    release_dt = datetime.strptime(dm.group(1), "%B %d, %Y").date()
    tm = re.search(r"For release at\s+(\d{1,2}:\d{2})\s*a\.m\.\s*\(([^)]+)\)", release_line, flags=re.I)
    if not tm:
        raise ValueError("9:15 a.m. release timestamp not found")
    release_clock, tz_label = tm.groups()

    ip_idx = next(i for i, ln in enumerate(lines) if ln.strip().startswith("Industrial production") and "|" in ln)
    cu_idx = next(i for i, ln in enumerate(lines) if ln.strip().startswith("Capacity utilization") and "|" in ln)
    obs_month_short = _last_month_header(lines[ip_idx])
    month_num = datetime.strptime(obs_month_short[:3], "%b").month
    obs_year = release_dt.year if month_num < release_dt.month or release_dt.month == 1 else release_dt.year - 1
    # December released in January belongs to prior year.
    if release_dt.month == 1 and month_num == 12:
        obs_year = release_dt.year - 1
    observation_month = date(obs_year, month_num, 1).isoformat()[:7]

    total_index, total_mom = _parse_table_row(lines, ip_idx, "Total index")
    mfg_index, mfg_mom = _parse_table_row(lines, ip_idx, "Manufacturing")
    total_cu = _parse_capacity_row(lines, cu_idx, "Total industry")
    mfg_cu = _parse_capacity_row(lines, cu_idx, "Manufacturing")
    required = [total_index, total_mom, total_cu]
    if any(x is None for x in required):
        raise ValueError("required total IP/CU values not parsed")
    assert total_index is not None
    assert total_mom is not None
    assert total_cu is not None
    return G17FirstVintageEvent(
        release_date=release_dt.isoformat(),
        release_time_et=release_clock,
        release_timezone_label=tz_label,
        observation_month=observation_month,
        official_text_url=url,
        indpro_total_index=float(total_index),
        indpro_total_mom_pct=float(total_mom),
        capacity_utilization_total=float(total_cu),
        capacity_utilization_total_change_pp=None,
        manufacturing_index=float(mfg_index) if mfg_index is not None else None,
        manufacturing_mom_pct=float(mfg_mom) if mfg_mom is not None else None,
        manufacturing_capacity_utilization=float(mfg_cu) if mfg_cu is not None else None,
    )


def build_sample_event_table(limit: int = 24, start_yyyymmdd: str = "20010201") -> list[dict[str, object]]:
    """Fetch official archive index and parse a bounded sample of dated releases."""
    index_html = fetch_url(BASE_URL)
    links = list_archive_text_links(index_html, start_yyyymmdd=start_yyyymmdd)
    if not links:
        raise ValueError("no official G.17 dated g17.txt links found")
    if limit and len(links) > limit:
        step = max(1, len(links) // limit)
        sample_links = links[::step][:limit]
    else:
        sample_links = links
    events = [parse_g17_release_text(fetch_url(link), link) for link in sample_links]
    return [asdict(event) for event in events]


if __name__ == "__main__":  # small live smoke, no raw downloads retained
    import json

    print(json.dumps(build_sample_event_table(limit=6), indent=2, sort_keys=True))
