"""
filters.py — Location and title/department filtering logic.

No server-side filtering exists on the Greenhouse public API.
Everything is done client-side here.
"""""
filters.py — Location and title/department filtering logic.

No server-side filtering exists on the Greenhouse public API.
Everything is done client-side here.
"""

import re


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
    Any non-USA country/region mentioned = rejected immediately.
    """
    if not location or location.strip() == "":
        return True

    loc = location.strip()

    if _NON_USA_RE.search(loc):
        return False

    if _USA_RE.search(loc):
        return True

    return False


# ---------------------------------------------------------------------------
# Title / department filtering — CYBERSECURITY ENTRY & MID LEVEL ONLY
# ---------------------------------------------------------------------------

INCLUDE_KEYWORDS = [

    # ── SOC & Incident Response ──────────────────────────────────────
    "soc analyst",
    "soc engineer",
    "security operations center",
    "security operations analyst",
    "security operations engineer",
    "incident response",
    "incident responder",
    "incident investigation",
    "alert triage",
    "threat detection",
    "threat intelligence",
    "threat analyst",
    "threat hunter",
    "ioc analysis",
    "log correlation",
    "mitre att&ck",

    # ── SIEM & EDR Tools ─────────────────────────────────────────────
    "splunk",
    "siem",
    "edr",
    "soar",
    "crowdstrike",
    "ids analyst",
    "ips analyst",

    # ── Core Security Roles ───────────────────────────────────────────
    "security analyst",
    "security engineer",
    "security researcher",
    "cybersecurity analyst",
    "cybersecurity engineer",
    "cyber security analyst",
    "cyber security engineer",
    "infosec analyst",
    "information security analyst",
    "information security engineer",

    # ── Cloud Security ────────────────────────────────────────────────
    "cloud security analyst",
    "cloud security engineer",
    "aws security",
    "cloud security",

    # ── AppSec / Vulnerability ────────────────────────────────────────
    "application security analyst",
    "application security engineer",
    "vulnerability analyst",
    "vulnerability management",
    "penetration tester",
    "penetration analyst",
    "pentest",
    "blue team analyst",
    "blue team engineer",

    # ── Malware / Forensics ───────────────────────────────────────────
    "malware analyst",
    "malware researcher",
    "digital forensics",
    "forensics analyst",
    "phishing analyst",

    # ── GRC / Compliance ──────────────────────────────────────────────
    "grc analyst",
    "grc engineer",
    "security compliance analyst",
    "security compliance engineer",
    "security risk analyst",
    "information security compliance",
    "cyber risk analyst",

    # ── Network / Endpoint Security ───────────────────────────────────
    "network security analyst",
    "network security engineer",
    "endpoint security analyst",
    "endpoint security engineer",
    "zero trust analyst",

    # ── IAM / Identity Security ───────────────────────────────────────
    "identity security analyst",
    "identity security engineer",
    "iam analyst",
    "iam engineer",
    "identity and access management analyst",
    "identity and access management engineer",

]

# ---------------------------------------------------------------------------
# Seniority — EXCLUDED title patterns (too senior for entry/mid level)
# ---------------------------------------------------------------------------

EXCLUDE_SENIORITY_PATTERNS = [
    "director",
    "vp ",
    "vice president",
    "head of",
    "chief",
    "cto", "ciso", "coo", "ceo",
    "principal",
    "staff ",
    "senior manager",
    "sr. manager",
    "sr manager",
    "senior director",
    "sr. director",
    "sr director",
    "associate director",
    "managing director",
    "executive director",
    "president",
    "fellow",
    "lead ",        # "Lead Engineer", "Lead Analyst" — too senior
    " lead",        # trailing lead e.g. "Security Lead"
    "manager",      # catches all manager variants not already covered
]

# ---------------------------------------------------------------------------
# Non-security roles — EXCLUDED even if a security keyword accidentally matches
# ---------------------------------------------------------------------------

EXCLUDE_ROLE_PATTERNS = [
    "physical security",
    "campus security",
    "corporate security manager",
    "security counsel",
    "security attorney",
    "security sales",
    "security marketing",
    "security program manager",
    "security project manager",
    "software engineer",
    "software developer",
    "product engineer",
    "product manager",
    "product designer",
    "product security manager",   # manager = too senior
    "program manager",
    "account executive",
    "account manager",
    "sales",
    "marketing",
    "partnerships",
    "recruiter",
    "administrative",
    "operations intern",
    "fund accountant",
    "legal counsel",
    "data scientist",
    "android engineer",
    "ios engineer",
    "frontend engineer",
    "backend engineer",
    "fullstack engineer",
    "full stack engineer",
    "ml engineer",
    "research scientist",
    "research engineer",
    "blockchain engineer",
    "blockchain security engineer",  # very niche/non-SOC
    "geopolitical",
    "crisis management",
    "insider risk investigator",     # intelligence/investigator = not SOC
    "physical",
    "executive protection",
    "helpdesk",
    "help desk",
    "it support",
    "business analyst",
    "data analyst",
    "fraud specialist",
    "compliance officer",            # legal compliance, not security
    "strategy and operations",
]

_INCLUDE_RE = re.compile(
    "|".join(re.escape(k) for k in INCLUDE_KEYWORDS),
    re.IGNORECASE,
)

_EXCLUDE_SENIORITY_RE = re.compile(
    "|".join(re.escape(k) for k in EXCLUDE_SENIORITY_PATTERNS),
    re.IGNORECASE,
)

_EXCLUDE_ROLE_RE = re.compile(
    "|".join(re.escape(k) for k in EXCLUDE_ROLE_PATTERNS),
    re.IGNORECASE,
)


def is_software_role(title: str, department: str = "") -> bool:
    """
    Returns True ONLY for entry/mid-level cybersecurity roles.
    Rejects: too-senior titles, non-security roles, physical/legal/sales security.
    """
    # Step 1 — reject non-security roles immediately
    if _EXCLUDE_ROLE_RE.search(title):
        return False

    # Step 2 — reject too-senior titles
    if _EXCLUDE_SENIORITY_RE.search(title):
        return False

    # Step 3 — must match a cybersecurity include keyword
    combined = f"{title} {department}"
    if not _INCLUDE_RE.search(combined):
        return False

    return True


def is_entry_mid_level(title: str) -> bool:
    """
    Returns True if the title is entry or mid level.
    Called separately from poller.py if needed.
    """
    return not bool(_EXCLUDE_SENIORITY_RE.search(title))

import re


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
    Any non-USA country/region mentioned = rejected immediately.
    """
    if not location or location.strip() == "":
        return True  # blank = assume remote/unspecified → include

    loc = location.strip()

    if _NON_USA_RE.search(loc):
        return False

    if _USA_RE.search(loc):
        return True

    return False


# ---------------------------------------------------------------------------
# Title / department filtering — CYBERSECURITY & SOC ROLES ONLY
# ---------------------------------------------------------------------------

# These keywords MUST match for a job to be included
INCLUDE_KEYWORDS = [

    # ── SOC & Incident Response ──────────────────────────────────────
    "soc analyst",
    "soc engineer",
    "security operations center",
    "security operations analyst",
    "security operations engineer",
    "incident response",
    "incident responder",
    "incident investigation",
    "alert triage",
    "threat detection",
    "threat intelligence",
    "threat analyst",
    "threat hunter",
    "ioc analysis",
    "log correlation",
    "mitre att&ck",
    "playbook",

    # ── SIEM & EDR Tools ─────────────────────────────────────────────
    "splunk",
    "siem",
    "edr",
    "soar", "crowdstrike", 
    "ids", "ips",

    # ── Core Security Roles ───────────────────────────────────────────
    "security analyst",
    "security engineer",
    "security researcher",
    "cybersecurity analyst",
    "cybersecurity engineer",
    "cyber security analyst",
    "cyber security engineer",
    "infosec analyst",
    "information security analyst",

    # ── Cloud Security ────────────────────────────────────────────────
    "cloud security analyst",
    "cloud security",

    # ── AppSec / Vulnerability ────────────────────────────────────────
    
    "vulnerability",
     "blue team",
    

    # ── Malware / Forensics ───────────────────────────────────────────
    "malware analyst",
    "malware researcher",
    "digital forensics",
    "forensics analyst",
    "phishing analyst",

    # ── GRC / Compliance ──────────────────────────────────────────────
    "grc analyst",
    "grc engineer",
    "compliance analyst",
    "risk analyst",
    "security compliance",
    "security risk",

    # ── Network / Endpoint Security ───────────────────────────────────
    "network security",
    "endpoint security",
    "zero trust",

    # ── IAM / Identity Security ───────────────────────────────────────
    "identity security",
    "identity and access",
    "iam analyst",
    "iam engineer",

]

# These title patterns are EXCLUDED even if include keywords match
# Removes senior leadership, non-technical, and physical security roles
EXCLUDE_TITLE_PATTERNS = [
    "physical security",
    "campus security",
    "corporate security",
    "security counsel",
    "security attorney",
    "security sales",
    "security marketing",
    "security program manager",
    "security project manager",
    "director",
    "vp ",
    "vice president",
    "head of",
    "chief",
    "cto", "ciso", "coo", "ceo",
    "principal",
    "staff ",
    "senior manager",
    "sr. manager",
    "sr manager",
    "senior director",
    "sr. director",
    "sr director",
    "associate director",
    "managing director",
    "executive director",
    "president",
    "partner",
]

_INCLUDE_RE = re.compile(
    "|".join(re.escape(k) for k in INCLUDE_KEYWORDS),
    re.IGNORECASE,
)

_EXCLUDE_RE = re.compile(
    "|".join(re.escape(k) for k in EXCLUDE_TITLE_PATTERNS),
    re.IGNORECASE,
)


def is_software_role(title: str, department: str = "") -> bool:
    """
    Returns True if the job is a cybersecurity/SOC role.
    Excludes leadership, physical security, and non-technical roles.
    """
    combined = f"{title} {department}"

    # Must match an include keyword
    if not _INCLUDE_RE.search(combined):
        return False

    # Must NOT match an exclude pattern
    if _EXCLUDE_RE.search(title):
        return False

    return True


# ---------------------------------------------------------------------------
# Seniority filtering — kept for reference but applied inside is_software_role
# ---------------------------------------------------------------------------

def is_entry_mid_level(title: str) -> bool:
    """
    Returns True if the job is entry or mid level.
    Senior Engineer/Analyst is kept — that's still mid-level.
    """
    return not bool(_EXCLUDE_RE.search(title))
