#!/usr/bin/env python3
"""
job_scraper.py – Daily job scraper for Cloud / Network / Systems roles.
Posts new listings to a Discord channel via webhook.

Sources
-------
* LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs  – via python-jobspy
* RemoteOK    – public JSON API (https://remoteok.com/api)
* Arbeitnow   – free European tech API (no key needed)
* Adzuna      – free API, strong NL coverage (requires ADZUNA_APP_ID + ADZUNA_API_KEY)

Managed by Ansible – do not edit by hand.
"""

import os
import math
import sqlite3
import logging
import time
from datetime import datetime
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration (from environment / systemd EnvironmentFile)
# ---------------------------------------------------------------------------

DISCORD_WEBHOOKS: dict[str, str] = {
    "☁️ Cloud Engineering":    os.environ["DISCORD_WEBHOOK_CLOUD"],
    "🌐 Network Engineering":  os.environ["DISCORD_WEBHOOK_NETWORKING"],
    "⚙️ Systems Engineering": os.environ["DISCORD_WEBHOOK_SYSTEMS"],
    "🏛️ Architecture":         os.environ["DISCORD_WEBHOOK_ARCHITECTURE"],
    "👑 Lead Engineering":     os.environ["DISCORD_WEBHOOK_LEAD_ENGINEERING"],
    "🔧 DevOps":               os.environ["DISCORD_WEBHOOK_DEVOPS"],
}
DB_PATH = Path(os.environ.get("JOB_SCRAPER_DB", "/var/lib/job-scraper/jobs.db"))
RESULTS_PER_QUERY = int(os.environ.get("RESULTS_PER_QUERY", "15"))
COUNTRY = os.environ.get("COUNTRY", "USA")
LOCATION = os.environ.get("LOCATION", "")

# ---------------------------------------------------------------------------
# Search taxonomy
# ---------------------------------------------------------------------------

SEARCH_QUERIES: dict[str, list[str]] = {
    "☁️ Cloud Engineering": [
        "cloud engineer",
        "devops engineer",
        "platform engineer",
        "site reliability engineer",
    ],
    "🌐 Network Engineering": [
        "network engineer",
        "network administrator",
        "NOC engineer",
    ],
    "⚙️ Systems Engineering": [
        "systems engineer",
        "systems administrator",
        "linux administrator",
        "infrastructure engineer",
    ],
    "🏛️ Architecture": [
        "network architect",
        "security architect",
        "solutions architect",
        "systems architect",
        "enterprise architect",
    ],
    "👑 Lead Engineering": [
        "lead engineer",
        "principal engineer",
        "staff engineer",
        "engineering manager",
        "technical lead",
    ],
    "🔧 DevOps": [
        "devops engineer",
        "devsecops engineer",
        "CI/CD engineer",
        "release engineer",
        "GitOps engineer",
    ],
}

JOBSPY_SITES = ["linkedin", "indeed", "glassdoor", "google"]

# Adzuna (optional – leave blank to skip)
ADZUNA_APP_ID  = os.environ.get("ADZUNA_APP_ID", "")
ADZUNA_API_KEY = os.environ.get("ADZUNA_API_KEY", "")
ADZUNA_COUNTRY = os.environ.get("ADZUNA_COUNTRY", "nl")  # nl = Netherlands

CATEGORY_COLORS: dict[str, int] = {
    "☁️ Cloud Engineering":    0x5865F2,
    "🌐 Network Engineering":  0x57F287,
    "⚙️ Systems Engineering": 0xFEE75C,
    "🏛️ Architecture":         0xED4245,
    "👑 Lead Engineering":     0xFEA500,
    "🔧 DevOps":               0x00B0F4,
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------


def init_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS seen_jobs (
            job_id   TEXT PRIMARY KEY,
            title    TEXT,
            company  TEXT,
            added_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def is_new(conn: sqlite3.Connection, job_id: str) -> bool:
    return (
        conn.execute(
            "SELECT 1 FROM seen_jobs WHERE job_id = ?", (job_id,)
        ).fetchone()
        is None
    )


def mark_seen(
    conn: sqlite3.Connection, job_id: str, title: str, company: str
) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO seen_jobs (job_id, title, company, added_at)"
        " VALUES (?, ?, ?, ?)",
        (job_id, title, company, datetime.utcnow().isoformat()),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def _safe(val) -> str:
    """Return val as str, mapping NaN / None to empty string."""
    if val is None:
        return ""
    try:
        if isinstance(val, float) and math.isnan(val):
            return ""
    except Exception:
        pass
    s = str(val)
    return "" if s in ("nan", "None", "NaT") else s


# ---------------------------------------------------------------------------
# Job fetchers
# ---------------------------------------------------------------------------


def fetch_jobspy(category: str, query: str) -> list[dict]:
    """Scrape LinkedIn, Indeed, and Glassdoor via python-jobspy."""
    try:
        from jobspy import scrape_jobs  # type: ignore
        import pandas as pd  # type: ignore

        df = scrape_jobs(
            site_name=JOBSPY_SITES,
            search_term=query,
            results_wanted=RESULTS_PER_QUERY,
            country_indeed=COUNTRY,
            location=LOCATION or None,
            hours_old=25,  # slightly over 24 h to avoid edge-case misses
        )
        if df is None or df.empty:
            return []

        jobs: list[dict] = []
        for _, row in df.iterrows():
            raw_id = _safe(row.get("id")) or (
                f"{row.get('title','')}-{row.get('company','')}"
            )
            job_id = f"jobspy_{abs(hash(raw_id)) % (10**12)}"

            salary = ""
            min_amt = row.get("min_amount")
            max_amt = row.get("max_amount")
            if pd.notna(min_amt) and min_amt:
                salary = f"${float(min_amt):,.0f}"
                if pd.notna(max_amt) and max_amt:
                    salary += f" – ${float(max_amt):,.0f}"

            jobs.append(
                {
                    "id": job_id,
                    "title": _safe(row.get("title")),
                    "company": _safe(row.get("company")),
                    "location": _safe(row.get("location")),
                    "job_type": _safe(row.get("job_type")),
                    "salary": salary,
                    "url": _safe(row.get("job_url")),
                    "date_posted": _safe(row.get("date_posted")),
                    "source": _safe(row.get("site")).capitalize(),
                    "category": category,
                }
            )
        return jobs

    except Exception as exc:
        log.warning("jobspy error for %r (%s): %s", query, category, exc)
        return []


def fetch_remoteok(category: str, keywords: list[str]) -> list[dict]:
    """Fetch matching jobs from RemoteOK's public JSON API."""
    try:
        resp = requests.get(
            "https://remoteok.com/api",
            headers={"User-Agent": "job-scraper/1.0 (self-hosted lab tool)"},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        # First element is a legal/metadata notice – skip it
        postings = [
            item
            for item in data
            if isinstance(item, dict) and "position" in item
        ]

        kw_lower = [k.lower() for k in keywords]
        jobs: list[dict] = []

        for job in postings:
            text = (
                job.get("position", "")
                + " "
                + " ".join(job.get("tags") or [])
            ).lower()
            if not any(kw in text for kw in kw_lower):
                continue

            salary = ""
            s_min = job.get("salary_min")
            s_max = job.get("salary_max")
            if s_min:
                salary = f"${int(s_min):,}"
                if s_max:
                    salary += f" – ${int(s_max):,}"

            job_url = job.get("url", "")
            jobs.append(
                {
                    "id": f"remoteok_{job.get('id', abs(hash(job_url)))}",
                    "title": job.get("position", ""),
                    "company": job.get("company", ""),
                    "location": "Remote",
                    "job_type": "Full-time",
                    "salary": salary,
                    "url": job_url,
                    "date_posted": (job.get("date") or "")[:10],
                    "source": "RemoteOK",
                    "category": category,
                }
            )
        return jobs

    except Exception as exc:
        log.warning("RemoteOK error for %s: %s", category, exc)
        return []


def fetch_arbeitnow(category: str, keywords: list[str]) -> list[dict]:
    """Fetch matching jobs from Arbeitnow's free public API (European tech roles)."""
    try:
        jobs: list[dict] = []
        page = 1
        kw_lower = [k.lower() for k in keywords]

        while page <= 3:  # cap at 3 pages (75 listings) per category
            resp = requests.get(
                "https://www.arbeitnow.com/api/job-board-api",
                params={"page": page},
                headers={"Accept": "application/json"},
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json().get("data", [])
            if not data:
                break

            for job in data:
                text = (
                    job.get("title", "") + " " + " ".join(
                        str(t) for t in (job.get("tags") or []) if isinstance(t, str)
                    )
                ).lower()
                if not any(kw in text for kw in kw_lower):
                    continue

                slug = job.get("slug", "")
                jobs.append(
                    {
                        "id": f"arbeitnow_{slug or abs(hash(job.get('url', '')))}",
                        "title": job.get("title", ""),
                        "company": job.get("company_name", ""),
                        "location": job.get("location", "Remote"),
                        "job_type": "Full-time" if job.get("employment_type") in (None, "FULLTIME") else job.get("employment_type", ""),
                        "salary": "",
                        "url": job.get("url", ""),
                        "date_posted": str(job.get("created_at") or "")[:10],
                        "source": "Arbeitnow",
                        "category": category,
                    }
                )
            page += 1
            time.sleep(1)

        return jobs

    except Exception as exc:
        log.warning("Arbeitnow error for %s: %s", category, exc)
        return []


def fetch_adzuna(category: str, keywords: list[str]) -> list[dict]:
    """Fetch jobs from Adzuna API. Skipped if ADZUNA_APP_ID / ADZUNA_API_KEY not set."""
    if not ADZUNA_APP_ID or not ADZUNA_API_KEY:
        return []

    jobs: list[dict] = []
    try:
        for kw in keywords:
            resp = requests.get(
                f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/1",
                params={
                    "app_id": ADZUNA_APP_ID,
                    "app_key": ADZUNA_API_KEY,
                    "what": kw,
                    "results_per_page": RESULTS_PER_QUERY,
                    "content-type": "application/json",
                },
                timeout=20,
            )
            resp.raise_for_status()
            for job in resp.json().get("results", []):
                job_id = f"adzuna_{job.get('id', abs(hash(job.get('redirect_url', ''))))}"
                salary = ""
                s_min = job.get("salary_min")
                s_max = job.get("salary_max")
                if s_min:
                    salary = f"€{int(s_min):,}"
                    if s_max:
                        salary += f" – €{int(s_max):,}"
                jobs.append(
                    {
                        "id": job_id,
                        "title": job.get("title", ""),
                        "company": (job.get("company") or {}).get("display_name", ""),
                        "location": (job.get("location") or {}).get("display_name", ""),
                        "job_type": "Full-time",
                        "salary": salary,
                        "url": job.get("redirect_url", ""),
                        "date_posted": (job.get("created") or "")[:10],
                        "source": "Adzuna",
                        "category": category,
                    }
                )
            time.sleep(1)
    except Exception as exc:
        log.warning("Adzuna error for %s: %s", category, exc)

    return jobs


# ---------------------------------------------------------------------------
# Discord helpers
# ---------------------------------------------------------------------------


def build_embed(job: dict) -> dict:
    color = CATEGORY_COLORS.get(job["category"], 0x99AAB5)
    fields = [
        {"name": "Company", "value": job["company"] or "Unknown", "inline": True},
        {
            "name": "Location",
            "value": job["location"] or "Remote / Unspecified",
            "inline": True,
        },
        {"name": "Source", "value": job["source"], "inline": True},
    ]
    if job.get("job_type"):
        fields.append({"name": "Type", "value": job["job_type"], "inline": True})
    if job.get("salary"):
        fields.append({"name": "Salary", "value": job["salary"], "inline": True})

    embed: dict = {
        "title": job["title"][:256],
        "color": color,
        "fields": fields,
        "footer": {
            "text": f"{job['category']}  •  {job.get('date_posted') or 'Today'}"
        },
    }
    if job.get("url"):
        embed["url"] = job["url"]
    return embed


def post_summary(counts: dict[str, int], total: int) -> None:
    """Post a run-summary embed to every channel."""
    run_date = datetime.utcnow().strftime("%d %b %Y")
    fields = [
        {"name": cat, "value": f"{n} new listing(s)", "inline": False}
        for cat, n in counts.items()
    ]
    fields.append({"name": "─" * 20, "value": f"**Total: {total} new listing(s)**", "inline": False})

    embed = {
        "title": f"📋 Daily Job Summary — {run_date}",
        "color": 0xEB459E,
        "fields": fields,
        "footer": {"text": "Next run: tomorrow at 08:00 UTC"},
    }

    for category, webhook_url in DISCORD_WEBHOOKS.items():
        resp = requests.post(webhook_url, json={"embeds": [embed]}, timeout=15)
        if resp.status_code not in (200, 204):
            log.error(
                "Summary webhook error for %s: %d %s",
                category,
                resp.status_code,
                resp.text[:200],
            )
        time.sleep(1.0)


def post_batch(embeds: list[dict], category: str, header: str | None = None) -> None:
    """POST embeds to the correct Discord channel in batches of 10 (API limit)."""
    webhook_url = DISCORD_WEBHOOKS[category]
    for i in range(0, len(embeds), 10):
        batch = embeds[i : i + 10]
        payload: dict = {"embeds": batch}
        if i == 0 and header:
            payload["content"] = header
        resp = requests.post(webhook_url, json=payload, timeout=15)
        if resp.status_code not in (200, 204):
            log.error(
                "Discord webhook returned %d: %s",
                resp.status_code,
                resp.text[:300],
            )
        time.sleep(1.5)  # stay under the 30 req/min rate limit


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    conn = init_db()
    total_new = 0
    counts: dict[str, int] = {}

    for category, queries in SEARCH_QUERIES.items():
        new_jobs: list[dict] = []

        # --- jobspy: LinkedIn, Indeed, Glassdoor ---
        for query in queries:
            log.info("Fetching [%s] → %s", category, query)
            for job in fetch_jobspy(category, query):
                if is_new(conn, job["id"]):
                    new_jobs.append(job)
                    mark_seen(conn, job["id"], job["title"], job["company"])

        # --- RemoteOK ---
        log.info("Fetching RemoteOK → %s", category)
        for job in fetch_remoteok(category, queries):
            if is_new(conn, job["id"]):
                new_jobs.append(job)
                mark_seen(conn, job["id"], job["title"], job["company"])

        # --- Arbeitnow ---
        log.info("Fetching Arbeitnow → %s", category)
        for job in fetch_arbeitnow(category, queries):
            if is_new(conn, job["id"]):
                new_jobs.append(job)
                mark_seen(conn, job["id"], job["title"], job["company"])

        # --- Adzuna ---
        log.info("Fetching Adzuna → %s", category)
        for job in fetch_adzuna(category, queries):
            if is_new(conn, job["id"]):
                new_jobs.append(job)
                mark_seen(conn, job["id"], job["title"], job["company"])

        if new_jobs:
            log.info("Posting %d new jobs for %s", len(new_jobs), category)
            embeds = [build_embed(j) for j in new_jobs]
            post_batch(embeds, category=category, header=f"**{category}** — {len(new_jobs)} new listing(s)")
            total_new += len(new_jobs)
        else:
            log.info("No new listings for %s", category)

        counts[category] = len(new_jobs)

    post_summary(counts, total_new)
    log.info("Run complete. Total new jobs posted: %d", total_new)
    conn.close()


if __name__ == "__main__":
    main()
