"""
scorer.py — Resume match scoring.
Primary: Groq API (free tier) — llama-3.3-70b-versatile
Fallback: Anthropic Claude Haiku (if Groq fails or key missing)
"""

import os
import re
import time
import requests
from pathlib import Path
from typing import Optional

# --- Groq config ---
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

# --- Anthropic config ---
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"

SCORE_THRESHOLD = 65
MAX_RETRIES = 2
RETRY_DELAY = 5

RESUME_FILE = Path("resume.txt")
_resume_cache: Optional[str] = None


def _load_resume() -> str:
    global _resume_cache
    if _resume_cache is None:
        if not RESUME_FILE.exists():
            raise FileNotFoundError(f"resume.txt not found at {RESUME_FILE.absolute()}")
        _resume_cache = RESUME_FILE.read_text(encoding="utf-8").strip()
    return _resume_cache


def _build_prompt(job_title: str, company: str, description: str) -> str:
    resume = _load_resume()
    return f"""You are a strict technical recruiter evaluating resume-to-job fit.

Score this resume against the job using the 4 criteria below.
Internally evaluate each criterion, then output ONLY a single integer from 0 to 100 as your final weighted score.
Do not output anything else — no explanation, no breakdown, just the integer.

SCORING CRITERIA (evaluate internally before giving final score):
1. Technical skills match — languages, frameworks, tools, cloud (weight: 40%)
2. Domain and industry fit — fintech, banking, distributed systems, microservices (weight: 25%)
3. Seniority level match — junior/mid/senior/staff alignment (weight: 20%)
4. Years of experience alignment — required vs actual (weight: 15%)

RESUME:
{resume}

JOB TITLE: {job_title}
COMPANY: {company}
JOB DESCRIPTION:
{description}

Final score (0-100 integer only):"""


def _parse_score(raw_text: str) -> Optional[int]:
    match = re.search(r'\b(\d{1,3})\b', raw_text)
    if match:
        return max(0, min(100, int(match.group(1))))
    return None


def _score_with_groq(prompt: str) -> Optional[int]:
    key = os.environ.get("GROQ_GJT_API_KEY", "").strip()
    if not key:
        return None  # Groq not available, skip to fallback

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 20,
        "temperature": 0,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)

            if resp.status_code == 200:
                data = resp.json()
                raw_text = data["choices"][0]["message"]["content"].strip()
                usage = data.get("usage", {})
                print(f"  [groq] tokens: {usage.get('prompt_tokens','?')} in / {usage.get('completion_tokens','?')} out")
                return _parse_score(raw_text)

            elif resp.status_code == 429:
                wait = RETRY_DELAY * 2
                print(f"  [groq] Rate limited (attempt {attempt}), waiting {wait}s...")
                time.sleep(wait)

            elif resp.status_code in (500, 503):
                print(f"  [groq] Overloaded (attempt {attempt}), waiting {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)

            else:
                print(f"  [groq] Error {resp.status_code}: {resp.text[:200]}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"  [groq] Request error (attempt {attempt}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    return None


def _score_with_anthropic(prompt: str) -> Optional[int]:
    key = os.environ.get("CL_API_KEY", "").strip()
    if not key:
        return None  # Anthropic not available

    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 20,
        "messages": [{"role": "user", "content": prompt}],
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=30)

            if resp.status_code == 200:
                data = resp.json()
                raw_text = data["content"][0]["text"].strip()
                print(f"  [anthropic] response received")
                return _parse_score(raw_text)

            elif resp.status_code == 429:
                wait = RETRY_DELAY * 2
                print(f"  [anthropic] Rate limited (attempt {attempt}), waiting {wait}s...")
                time.sleep(wait)

            elif resp.status_code in (500, 503):
                print(f"  [anthropic] Overloaded (attempt {attempt}), waiting {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)

            else:
                print(f"  [anthropic] Error {resp.status_code}: {resp.text[:200]}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"  [anthropic] Request error (attempt {attempt}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    return None


def score_job(job: dict) -> Optional[int]:
    """Score a job against resume. Tries Groq first, falls back to Anthropic."""
    title = job.get("title", "")
    company = job.get("company", "")
    content = job.get("content", "") or ""
    description = _strip_html(content)

    if not description:
        description = f"No description available. Evaluate based on title only: {title}"

    prompt = _build_prompt(title, company, description)

    # Try Groq first
    print(f"  [scorer] Trying Groq...", end=" ", flush=True)
    score = _score_with_groq(prompt)
    if score is not None:
        print(f"✅ Groq scored: {score}")
        return score

    # Fall back to Anthropic
    print(f"  [scorer] Groq failed, trying Anthropic...", end=" ", flush=True)
    score = _score_with_anthropic(prompt)
    if score is not None:
        print(f"✅ Anthropic scored: {score}")
        return score

    print(f"  [scorer] Both scorers failed.")
    return None


def should_alert(score: int) -> bool:
    return score >= SCORE_THRESHOLD


def _strip_html(html: str) -> str:
    html = re.sub(r"<(br|p|li|tr|div|h[1-6])[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<[^>]+>", "", html)
    html = html.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    html = html.replace("&nbsp;", " ").replace("&#39;", "'").replace("&quot;", '"')
    html = re.sub(r"\n{3,}", "\n\n", html)
    html = re.sub(r" {2,}", " ", html)
    return html.strip()
