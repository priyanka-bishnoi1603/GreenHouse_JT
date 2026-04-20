"""
filters.py — Location and title/department filtering logic.
Tuned for: Priyanka Bishnoi — SOC Analyst | Cloud Security | IAM
Experience: Splunk, CrowdStrike, SentinelOne, AWS CloudTrail, GuardDuty, IAM, MITRE ATT&CK
Level: Entry to Mid level only (no Senior, Lead, Staff, Principal)
Extra: Excludes jobs requiring US Citizenship
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
    r"canada", r"australia", r"india",
    r"germany", r"berlin", r"munich",
    r"france", r"paris",
    r"netherlands", r"amsterdam",
    r"singapore", r"hong kong",
    r"japan", r"tokyo",
    r"brazil", r"mexico",
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
    if not location or location.strip() == "":
        return True
    loc = location.strip()
    if _NON_USA_RE.search(loc):
        return False
    if _USA_RE.search(loc):
        return True
    return False


# ---------------------------------------------------------------------------
# Title filtering — matched to Priyanka's resume
# ---------------------------------------------------------------------------

INCLUDE_KEYWORDS = [

    # SOC / Security Operations — her primary role
    "soc analyst",
    "soc engineer",
    "security operations analyst",
    "security operations engineer",
    "security operations center",
    "security analyst",
    "security engineer",
    "cybersecurity analyst",
    "cybersecurity engineer",
    "cyber security analyst",
    "cyber security engineer",
    "information security analyst",
    "information security engineer",
    "infosec analyst",

    # Incident Response — her core skill
    "incident response",
    "incident responder",
    "incident response analyst",
    "incident response engineer",
    "incident investigation",
    "detection and response",
    "detection & response",

    # Threat Detection / Intelligence — her daily work
    "threat detection",
    "threat intelligence",
    "threat analyst",
    "threat hunter",
    "threat hunting",
    "alert triage",
    "ioc analysis",
    "log correlation",

    # SIEM tools she knows
    "splunk",
    "siem",
    "siem analyst",
    "siem engineer",

    # EDR tools she knows
    "edr",
    "crowdstrike",
    "sentinelone",
    "microsoft defender",
    "endpoint security analyst",
    "endpoint security engineer",
    "endpoint detection",

    # Cloud Security — her second role at Yuno
    "cloud security analyst",
    "cloud security engineer",
    "cloud security",
    "aws security",
    "aws cloudtrail",
    "guardduty",
    "cloud detection",

    # IAM — her third role at Skyline
    "iam analyst",
    "iam engineer",
    "identity and access management analyst",
    "identity and access management engineer",
    "identity security analyst",
    "identity security engineer",
    "access management analyst",
    "access management engineer",

    # SOAR / Automation
    "soar",
    "security automation",
    "security orchestration",

    # Forensics / Malware — her coursework
    "digital forensics",
    "forensics analyst",
    "malware analyst",
    "phishing analyst",

    # Network Security
    "network security analyst",
    "network security engineer",

    # GRC / Compliance — her audit experience
    "grc analyst",
    "security compliance analyst",
    "cyber risk analyst",
    "information security compliance",

    # CSOC
    "csoc analyst",
    "csoc engineer",

    # Entry level specific
    "security engineer i",
    "security engineer ii",
    "security engineer 1",
    "security engineer 2",
    "associate security",
    "junior security",
    "new grad",
]


# ---------------------------------------------------------------------------
# Seniority exclusions — entry/mid only
# ---------------------------------------------------------------------------

EXCLUDE_SENIORITY_PATTERNS = [
    "senior",
    " sr ",
    "sr.",
    "lead",
    "staff",
    "principal",
    "architect",
    "director",
    "vp ",
    "vice president",
    "head of",
    "chief",
    "cto", "ciso", "coo", "ceo",
    "senior manager",
    "managing director",
    "executive director",
    "president",
    "fellow",
    "manager",
]


# ---------------------------------------------------------------------------
# Non-security / irrelevant role exclusions
# ---------------------------------------------------------------------------

EXCLUDE_ROLE_PATTERNS = [
    # Citizenship / clearance requirements (can't apply as visa holder)
    "us citizen",
    "u.s. citizen",
    "must be a us citizen",
    "requires us citizenship",
    "active clearance",
    "secret clearance",
    "top secret",
    "ts/sci",
    "sci clearance",
    "dod clearance",
    "security clearance required",
    "clearance required",
    "public trust",

    # Physical / non-technical security
    "physical security",
    "campus security",
    "corporate security manager",
    "executive protection",
    "geopolitical",
    "crisis management",
    "insider risk investigator",

    # Legal / business roles
    "security counsel",
    "security attorney",
    "security sales",
    "security marketing",
    "security program manager",
    "security project manager",

    # Engineering roles unrelated to security
    "software engineer",
    "software developer",
    "product engineer",
    "product manager",
    "product designer",
    "frontend engineer",
    "backend engineer",
    "fullstack engineer",
    "full stack engineer",
    "ml engineer",
    "android engineer",
    "ios engineer",
    "blockchain engineer",
    "research scientist",
    "research engineer",
    "data scientist",
    "data analyst",
    "data engineer", "blockchain security",
"corporate security",
"sap ",
"machine learning",
"phd",

    # Business / support roles
    "account executive",
    "account manager",
    "sales",
    "marketing",
    "partnerships",
    "recruiter",
    "administrative",
    "program manager",
    "business analyst",
    "fraud specialist",
    "compliance officer",
    "helpdesk",
    "help desk",
    "it support",
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


def is_software_role(title: str, department: str = "", description: str = "") -> bool:
    """
    Returns True ONLY for entry/mid-level cybersecurity roles
    matching Priyanka's background.
    Excludes US citizenship requirements, senior roles, non-security roles.
    """
    # Check title + description for citizenship requirements
    combined_check = f"{title} {description}"
    if _EXCLUDE_ROLE_RE.search(combined_check):
        return False

    # Check seniority in title only
    if _EXCLUDE_SENIORITY_RE.search(title):
        return False

    # Must match an include keyword in title or department
    combined = f"{title} {department}"
    if not _INCLUDE_RE.search(combined):
        return False

    return True


def is_entry_mid_level(title: str) -> bool:
    return not bool(_EXCLUDE_SENIORITY_RE.search(title))
