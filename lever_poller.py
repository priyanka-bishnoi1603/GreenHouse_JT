"""
lever_poller.py — Fetches jobs from Lever public API.
API: https://api.lever.co/v0/postings/{slug}?mode=json
No auth required.
"""

import requests
import time
from typing import Optional

LEVER_API_BASE = "https://api.lever.co/v0/postings/{slug}?mode=json"
REQUEST_TIMEOUT = 15
RETRY_ATTEMPTS = 2
RETRY_DELAY = 3


def fetch_lever_jobs(slug: str) -> Optional[list[dict]]:
    url = LEVER_API_BASE.format(slug=slug)
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                raw = resp.json()
                jobs = []
                for job in raw:
                    jobs.append({
                        "id": f"lever_{job.get('id', '')}",
                        "title": job.get("text", ""),
                        "company": slug,
                        "updated_at": job.get("updatedAt", ""),
                        "absolute_url": job.get("hostedUrl", ""),
                        "location": {"name": job.get("categories", {}).get("location", "")},
                        "departments": [{"name": job.get("categories", {}).get("department", "")}],
                        "_source": "lever",
                        "content": job.get("descriptionPlain", ""),
                    })
                return jobs
            elif resp.status_code == 404:
                print(f"  [skip] lever/{slug}: 404 — board not found.")
                return None
            else:
                print(f"  [warn] lever/{slug}: HTTP {resp.status_code} (attempt {attempt})")
        except requests.exceptions.Timeout:
            print(f"  [warn] lever/{slug}: timeout (attempt {attempt})")
        except requests.exceptions.RequestException as e:
            print(f"  [warn] lever/{slug}: {e} (attempt {attempt})")
        if attempt < RETRY_ATTEMPTS:
            time.sleep(RETRY_DELAY)
    return None
