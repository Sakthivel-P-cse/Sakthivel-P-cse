#!/usr/bin/env python3
import datetime as dt
import json
import os
import urllib.error
import urllib.request


LOG_PATH = "/home/sakthi/projects/github/.cursor/debug-b4ff50.log"
REPO = "Sakthivel-P-cse/Sakthivel-P-cse"
PAGES_BASE = "https://sakthivel-p-cse.github.io/Sakthivel-P-cse"
ASSETS = [
    "avi-ascii.svg",
    "info-card.svg",
    "contrib-heatmap.svg",
]


def log(hypothesis, message, data):
    entry = {
        "sessionId": "b4ff50",
        "runId": "initial",
        "hypothesisId": hypothesis,
        "location": "scripts/debug_profile_assets.py",
        "message": message,
        "data": data,
        "timestamp": int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000),
    }
    with open(LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def probe(label, url, hypothesis):
    request = urllib.request.Request(url, headers={"User-Agent": "sakthivel-profile-debug/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read(160).decode("utf-8", errors="replace")
            log(hypothesis, f"{label} response", {
                "status": response.status,
                "contentType": response.headers.get("Content-Type", ""),
                "retryAfter": response.headers.get("Retry-After", ""),
                "finalUrl": response.geturl(),
                "bodyPrefix": body[:120],
            })
    except urllib.error.HTTPError as error:
        body = error.read(160).decode("utf-8", errors="replace")
        log(hypothesis, f"{label} HTTP error", {
            "status": error.code,
            "contentType": error.headers.get("Content-Type", ""),
            "retryAfter": error.headers.get("Retry-After", ""),
            "finalUrl": error.geturl(),
            "bodyPrefix": body[:120],
        })
    except Exception as error:
        log(hypothesis, f"{label} request error", {
            "errorType": type(error).__name__,
            "error": str(error)[:160],
        })


if __name__ == "__main__":
    # region agent log
    log("H1", "asset probe started", {"assetCount": len(ASSETS)})
    # endregion
    for asset in ASSETS:
        # region agent log
        probe(
            f"raw sanitized {asset}",
            f"https://raw.githubusercontent.com/{REPO}/main/{asset}?sanitize=true",
            "H1",
        )
        # endregion
        # region agent log
        probe(
            f"raw plain {asset}",
            f"https://raw.githubusercontent.com/{REPO}/main/{asset}",
            "H3",
        )
        # endregion
        # region agent log
        probe(
            f"api metadata {asset}",
            f"https://api.github.com/repos/{REPO}/contents/{asset}",
            "H4",
        )
        # endregion
        # region agent log
        probe(
            f"pages asset {asset}",
            f"{PAGES_BASE}/{asset}",
            "H6",
        )
        # endregion
    # region agent log
    probe("pages root", f"{PAGES_BASE}/", "H7")
    # endregion
    # region agent log
    probe("pages index", f"{PAGES_BASE}/index.html", "H9")
    # endregion
    # region agent log
    probe(
        "contributions endpoint",
        "https://github.com/users/Sakthivel-P-cse/contributions",
        "H2",
    )
    # endregion
