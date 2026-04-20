"""
ashby_poller.py — Fetches jobs from Ashby public API.
API: https://api.ashbyhq.com/posting-api/job-board/{slug}
No auth required.
"""

import requests
import time
from typing import Optional

ASHBY_API_BASE = "https://api.ashbyhq.com/posting-api/job-board/{slug}"
REQUEST_TIMEOUT = 15
RETRY_ATTEMPTS = 2
RETRY_DELAY = 3


def fetch_ashby_jobs(slug: str) -> Optional[list[dict]]:
    url = ASHBY_API_BASE.format(slug=slug)
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                raw = resp.json().get("jobs", [])
                jobs = []
                for job in raw:
                    jobs.append({
                        "id": f"ashby_{job.get('id', '')}",
                        "title": job.get("title", ""),
                        "company": slug,
                        "updated_at": job.get("updatedAt", ""),
                        "absolute_url": job.get("jobUrl", ""),
                        "location": {"name": job.get("locationName", "")},
                        "departments": [{"name": job.get("department", "")}],
                        "_source": "ashby",
                        "content": job.get("descriptionPlain", ""),
                    })
                return jobs
            elif resp.status_code == 404:
                print(f"  [skip] ashby/{slug}: 404 — board not found.")
                return None
            else:
                print(f"  [warn] ashby/{slug}: HTTP {resp.status_code} (attempt {attempt})")
        except requests.exceptions.Timeout:
            print(f"  [warn] ashby/{slug}: timeout (attempt {attempt})")
        except requests.exceptions.RequestException as e:
            print(f"  [warn] ashby/{slug}: {e} (attempt {attempt})")
        if attempt < RETRY_ATTEMPTS:
            time.sleep(RETRY_DELAY)
    return None
