#!/usr/bin/env python3
import datetime as dt
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup


USERNAME = os.environ.get("GH_PROFILE_USER", "Sakthivel-P-cse")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, "data", "contributions.json")


def fetch_days():
    response = requests.get(
        f"https://github.com/users/{USERNAME}/contributions",
        headers={"User-Agent": "sakthivel-profile-art/1.0"},
        timeout=30,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        raise RuntimeError("GitHub contribution cells were not found")

    days = []
    for cell in cells:
        date = cell.get("data-date")
        if not date:
            continue
        cell_id = cell.get("id")
        tooltip = soup.find("tool-tip", attrs={"for": cell_id}) if cell_id else None
        tooltip_text = tooltip.get_text(" ", strip=True) if tooltip else ""
        match = re.search(r"(\d[\d,]*)\s+contribution", tooltip_text, re.IGNORECASE)
        count = int(match.group(1).replace(",", "")) if match else 0
        days.append({"date": date, "count": count})

    days.sort(key=lambda item: item["date"])
    if not days:
        raise RuntimeError("GitHub returned no dated contribution cells")
    return days


def streak(days):
    current = 0
    index = len(days) - 1
    if days[index]["count"] == 0:
        index -= 1
    while index >= 0 and days[index]["count"] > 0:
        current += 1
        index -= 1

    longest = 0
    run = 0
    for day in days:
        run = run + 1 if day["count"] > 0 else 0
        longest = max(longest, run)
    return current, longest


def build(days):
    total = sum(day["count"] for day in days)
    active = sum(day["count"] > 0 for day in days)
    best = max(days, key=lambda day: day["count"])
    current, longest = streak(days)
    monthly = {}
    for day in days:
        key = day["date"][:7]
        monthly[key] = monthly.get(key, 0) + day["count"]
    return {
        "username": USERNAME,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active,
        "avg_per_active_day": round(total / active, 1) if active else 0,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "monthly": [{"month": key, "total": value} for key, value in sorted(monthly.items())],
        "days": days,
    }


if __name__ == "__main__":
    try:
        data = build(fetch_days())
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    print(
        f"wrote {OUTPUT}: {data['total_contributions']} contributions, "
        f"{data['current_streak']} day current streak"
    )
