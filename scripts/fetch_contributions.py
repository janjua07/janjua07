#!/usr/bin/env python3
"""Fetch Ren's public GitHub contribution calendar without a token."""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "janjua07"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path("data/contributions.json")


def streaks(days: list[dict]) -> tuple[int, int]:
    active = [d["count"] > 0 for d in days]
    longest = run = 0
    for value in active:
        run = run + 1 if value else 0
        longest = max(longest, run)
    current = 0
    for value in reversed(active):
        if not value:
            break
        current += 1
    return current, longest


def main() -> None:
    response = requests.get(URL, headers={"User-Agent": "ren-profile-readme/1.0"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    for cell in soup.select("td[data-date][data-level]"):
        tooltip = soup.find("tool-tip", attrs={"for": cell.get("id")})
        text = tooltip.get_text(" ", strip=True) if tooltip else ""
        match = re.search(r"([0-9,]+) contribution", text)
        count = int(match.group(1).replace(",", "")) if match else 0
        days.append({
            "date": cell["data-date"],
            "count": count,
            "level": int(cell.get("data-level", 0)),
        })
    if len(days) < 350:
        raise RuntimeError(f"Expected a full contribution calendar, found only {len(days)} days")
    days.sort(key=lambda item: item["date"])
    current, longest = streaks(days)
    best = max(days, key=lambda item: item["count"])
    payload = {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total": sum(item["count"] for item in days),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "days": days,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"fetched {len(days)} days and {payload['total']} contributions -> {OUT}")


if __name__ == "__main__":
    main()
