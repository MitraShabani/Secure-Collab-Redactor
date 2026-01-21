import re
from typing import Tuple

# regex patterns for common sensitive data
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b")
IPV4_RE = re.compile(r"\b((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)\b")
API_KV_RE = re.compile(r"\bapi[_-]?key\s*=\s*[A-Za-z0-9_\-]{8,}\b", re.IGNORECASE)
API_KEY_RE = re.compile(r"\b(?:(?:api|secret|token|key)[_\-:]?\s*[A-Za-z0-9_\-]{16,})\b", re.IGNORECASE)
CC_RE = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
AWS_KEY_RE = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
JWT_RE = re.compile(r"\b[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{3,}\.[A-Za-z0-9_-]{3,}\b")

REDACTIONS = [
    ("AUTH_TOKEN", JWT_RE),
    ("CLOUD_ACCESS_KEY", AWS_KEY_RE),
    ("API_KEY", API_KV_RE),
    ("API_KEY", API_KEY_RE),
    ("EMAIL", EMAIL_RE),
    ("CREDIT_CARD", CC_RE),
    ("IPV4", IPV4_RE),
    ("PHONE", PHONE_RE),
]

def redact(text: str) -> Tuple[str, int]:
    """Run all patterns on text and replace matches with [REDACTED:<LABEL>:<len>]."""

    redactionCounter = 0
    redacted = text

    # replace matches with a labeled token
    for label, pattern in REDACTIONS:
        def repl(m):
            nonlocal redactionCounter
            redactionCounter += 1
            return f"[REDACTED:{label}:{len(m.group(0))}]"

        redacted = pattern.sub(repl, redacted)

    return redacted, redactionCounter