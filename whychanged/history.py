"""Answer the question weeks later: why is this setting what it is?"""
from .models import LogEntry


def history(entries: list[LogEntry], key: str) -> list[LogEntry]:
    """All entries for one setting, oldest first. Matches the full key or its last part."""
    hits = [e for e in entries if e.key == key or e.key.split(".")[-1] == key]
    return sorted(hits, key=lambda e: e.created_at)
