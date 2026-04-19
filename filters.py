"""
filters.py — Location and title/department filtering logic.

No server-side filtering exists on the Greenhouse public API.
Everything is done client-side here.
"""

import re


# Patterns that confirm a job is USA-based or USA-remote.
# Checked case-insensitively against the location string.
# ---------------------------------------------------------------------------
# Location filtering
# ---------------------------------------------------------------------------

USA_INCLUDE_PATTERNS = [
    r"\busa\b",
    r"\bus\b",
    r"united states",
    r"u\.s\.a",
    r"u\.s\.",
    r"remote.*us\b",
    r"\bus\b.*remote",
    r"remote.*united states",
    r"anywhere in the us",
    r"remote.*(usa|u\.s\.)",
    # common state names / abbreviations
    r"\bca\b", r"california",
    r"\bny\b", r"new york",
    r"\btx\b", r"texas",
    r"\bwa\b", r"washington",
    r"\bil\b", r"illinois",
    r"\bco\b", r"colorado",
    r"\bma\b", r"massachusetts",
    r"\bga\b", r"georgia",
    r"\bfl\b", r"florida",
    r"\bva\b", r"virginia",
    r"\bor\b", r"oregon",
    r"\baz\b", r"arizona",
    r"\bnc\b", r"north carolina",
    r"\bmn\b", r"minnesota",
    r"\boh\b", r"ohio",
    r"\bmi\b", r"michigan",
    r"\butah\b", r"\but\b",
    r"\bnv\b", r"nevada",
    r"san francisco", r"new york city", r"nyc", r"chicago",
    r"seattle", r"austin", r"boston", r"denver", r"atlanta",
    r"los angeles", r"\bla\b", r"miami", r"portland",
]

NON_USA_PATTERNS = [
    r"\buk\b", r"united kingdom", r"england", r"london",
    r"\beu\b", r"europe", r"european union",
    r"canada",
    r"australia",
    r"india",
    r"germany", r"berlin", r"munich",
    r"france", r"paris",
    r"netherlands", r"amsterdam",
    r"singapore", r"hong kong",
    r"japan", r"tokyo",
    r"brazil",
    r"mexico",
    r"ireland", r"dublin",
    r"poland", r"warsaw",
    r"sweden", r"stockholm",
    r"spain", r"madrid",
    r"israel", r"tel aviv",
    r"colombia", r"estonia", r"luxembourg",
    r"apac", r"emea", r"latam",
    r"south korea", r"korea",
    r"new zealand",
    r"switzerland", r"zurich",
    r"italy", r"milan", r"rome",
    r"portugal", r"lisbon",
    r"czech", r"prague",
    r"romania", r"bucharest",
    r"hungary", r"budapest",
    r"ukraine", r"kyiv",
    r"turkey", r"istanbul",
    r"south africa", r"johannesburg",
    r"nigeria", r"lagos",
    r"egypt", r"cairo",
    r"pakistan", r"karachi",
    r"bangladesh",
    r"philippines", r"manila",
    r"indonesia", r"jakarta",
    r"malaysia", r"kuala lumpur",
    r"thailand", r"bangkok",
    r"vietnam", r"ho chi minh",
    r"china", r"beijing", r"shanghai",
    r"taiwan", r"taipei",
]

_USA_RE = re.compile("|".join(USA_INCLUDE_PATTERNS), re.IGNORECASE)
_NON_USA_RE = re.compile("|".join(NON_USA_PATTERNS), re.IGNORECASE)


def is_usa_location(location: str) -> bool:
    """
    Returns True ONLY if the job is confirmed USA-based or USA-remote.
    Any non-USA country/region mentioned = rejected immediately, no exceptions.
    """
    if not location or location.strip() == "":
        return True  # blank = assume remote/unspecified → include

    loc = location.strip()

    # ANY non-USA signal → reject immediately, no exceptions
    if _NON_USA_RE.search(loc):
        return False

    # Must have a positive USA signal to pass
    if _USA_RE.search(loc):
        return True

    # Unknown location → exclude
    return False

# ---------------------------------------------------------------------------
# Title / department filtering — SOFTWARE & IT INCLUSION
# ---------------------------------------------------------------------------

# Broad allowlist: any job whose title OR department matches any of these
# passes through. Deliberately generous to avoid missing edge-case postings.

INCLUDE_KEYWORDS = [
  
 # ── SOC & Incident Response ──────────────────────────────────────
    "soc analyst", "soc engineer",
    "security operations",
    "incident response", "incident investigation",
    "alert triage", "threat detection",
    "threat intelligence",
    "ioc analysis",
    "log correlation",
    "case management",
    "mitre", "att&ck",
    "playbook",

    # ── SIEM & EDR ───────────────────────────────────────────────────
    "splunk",
    "siem",
    "edr",
    "crowdstrike",
    "sentinelone",
    "microsoft defender",
    "rapid7",
    "soar",
    "wireshark",
    "ids", "ips",

    # ── Cloud Security ───────────────────────────────────────────────
    "cloud security",
    "aws security",
    "cloudtrail",
    "guardduty",
    "cloud security analyst",
    "cloud security engineer",

    # ── IAM ──────────────────────────────────────────────────────────
    "identity and access",
    "iam",
    "active directory",
    "privileged access",
    "least privilege",
    "role-based access", "rbac",
    "access control",
    "identity governance",

    # ── Broad Security (catch-all) ────────────────────────────────────
    "security",           # ← ADDED — catches "Security Analyst", "Security Engineer" etc.
    "security analyst",
    "security engineer",
    "security operations analyst",
    "cybersecurity", "cyber security",
    "cybersecurity analyst",
    "cybersecurity engineer",
    "infosec",
    "information security",
    "appsec", "application security",
    "vulnerability",
    "malware",
    "phishing",
    "threat",
    "forensics", "digital forensics",
    "compliance",
    "risk analyst",
    "grc",
    "zero trust",
    "nist",
    "devsecops",
    "penetration", "pentesting",
    "red team", "blue team",
    "sast", "dast",
    "network security",
    "endpoint security",

    # ── Cloud Platforms (keep — security roles mention these) ─────────
    "aws", "gcp", "azure",

    # ── Technical Leadership (optional — remove if too noisy) ─────────
    "technical program",
    "technical lead",
    "tech lead",

    # ── IT (keep — covers IT Security, IT Analyst roles) ─────────────
    "information technology",
    
]

# Compile once — match against title + department combined
_INCLUDE_RE = re.compile(
    "|".join(re.escape(k) for k in INCLUDE_KEYWORDS),
    re.IGNORECASE,
)

# Separate word-boundary pattern for standalone "IT" — re.escape blocks \b
_IT_RE = re.compile(r"\bIT\b", re.IGNORECASE)


def is_software_role(title: str, department: str = "") -> bool:
    """
    Returns True if the job title or department suggests a software/IT role.
    """
    combined = f"{title} {department}"
    return bool(_INCLUDE_RE.search(combined) or _IT_RE.search(combined))


# ---------------------------------------------------------------------------
# Seniority filtering — ENTRY & MID LEVEL ONLY
# ---------------------------------------------------------------------------

EXCLUDE_SENIORITY = [
    "director", "vp ", "vice president",
    "head of", "chief", "cto", "ciso", "coo", "ceo",
    "principal",
    "staff ",
    "senior manager", "sr. manager", "sr manager",
    "senior director", "sr. director", "sr director",
    "associate director",
    "managing director",
    "executive",
    "president",
    "partner",
    "fellow",
]

_EXCLUDE_SENIORITY_RE = re.compile(
    "|".join(re.escape(k) for k in EXCLUDE_SENIORITY),
    re.IGNORECASE,
)

def is_entry_mid_level(title: str) -> bool:
    """
    Returns True if the job title is entry or mid level.
    Filters out Director, VP, Head, Principal, Staff, Senior Manager etc.
    Note: 'Senior Engineer/Analyst' alone is kept — that's still mid-level.
    """
    return not bool(_EXCLUDE_SENIORITY_RE.search(title))
