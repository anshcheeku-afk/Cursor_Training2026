"""Input validation helpers."""

from __future__ import annotations

import re

# Hostname / short name / IPv4 — no shell metacharacters
_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)"
    r"(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"|(?:\d{1,3}\.){3}\d{1,3})$"
)


def validate_hostname(hostname: str) -> str | None:
    """Return cleaned hostname or None if invalid."""
    if hostname is None:
        return None
    value = hostname.strip().lower()
    if not value or len(value) > 253:
        return None
    # Reject shell / path metacharacters explicitly
    if any(ch in value for ch in " ;|&$`\\\"'<>(){}[]!*?\n\r\t"):
        return None
    if not _HOSTNAME_RE.match(value):
        return None
    return value
