"""
notifier.py — Slack webhook alerter for Greenhouse Job Tracker.
Score is optional — works with or without resume scoring.
"""

import os
import json
import requests
from typing import Optional

SLACK_TIMEOUT = 10


def _get_webhook_url():
    url = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    return url if url else None


def _score_emoji(score: Optional[int]) -> str:
    if score is None:
        return "🆕"
    if score >= 85:
        return "🔥"
    elif score >= 70:
        return "🎯"
    elif score >= 65:
        return "✅"
    else:
        return "👀"


def _score_bar(score: Optional[int]) -> str:
    if score is None:
        return ""
    filled = round(score / 10)
    return "█" * filled + "░" * (10 - filled)


def send_slack_alert(job: dict, score: Optional[int] = None) -> bool:
    """Send a Slack alert for a job. Score is optional."""
    webhook_url = _get_webhook_url()
    if not webhook_url:
        print("  [slack] SLACK_WEBHOOK_URL not set — skipping alert.")
        return False

    title = job.get("title", "Unknown Title")
    company = job.get("company", "Unknown Company")
    location = job.get("_location", "Remote / Unspecified")
    url = job.get("_url", "")
    job_id = job.get("id", "")
    updated_at = job.get("updated_at", "")
    department = job.get("_department", "")

    emoji = _score_emoji(score)
    dept_text = f" · {department}" if department else ""

    # Build header text — with or without score
    if score is not None:
        bar = _score_bar(score)
        header_text = f"{emoji} {score}% Match — {title}"
        score_field = {"type": "mrkdwn", "text": f"*Score*\n`{bar}` {score}/100"}
        summary_text = f"{emoji} {score}% Match: {title} @ {company}"
    else:
        header_text = f"{emoji} New Job — {title}"
        score_field = None
        summary_text = f"{emoji} New Job: {title} @ {company}"

    fields = [
        {"type": "mrkdwn", "text": f"*Company*\n{company}{dept_text}"},
        {"type": "mrkdwn", "text": f"*Location*\n{location}"},
    ]
    if score_field:
        fields.append(score_field)

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": header_text,
                "emoji": True,
            },
        },
        {
            "type": "section",
            "fields": fields,
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "🔗 Apply Now", "emoji": True},
                    "url": url,
                    "style": "primary",
                }
            ],
        },
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"Job ID: `{job_id}` · Updated: `{updated_at}`"}
            ],
        },
        {"type": "divider"},
    ]

    payload = {
        "text": summary_text,
        "blocks": blocks,
    }

    try:
        resp = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=SLACK_TIMEOUT,
        )
        if resp.status_code == 200:
            print(f"  [slack] ✅ Alert sent: {title} @ {company}")
            return True
        else:
            print(f"  [slack] ❌ Failed ({resp.status_code}): {resp.text[:100]}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"  [slack] ❌ Request error: {e}")
        return False


def send_run_summary(stats: dict) -> bool:
    webhook_url = _get_webhook_url()
    if not webhook_url:
        return False

    payload = {
        "text": (
            f"📊 *Job Poll Summary* — "
            f"{stats.get('jobs_new', 0)} new · "
            f"{stats.get('jobs_updated', 0)} updated · "
            f"{stats.get('alerts_sent', 0)} alerts sent · "
            f"{stats.get('elapsed', 0)}s elapsed"
        )
    }

    try:
        resp = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=SLACK_TIMEOUT,
        )
        return resp.status_code == 200
    except Exception:
        return False
