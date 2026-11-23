"""Which watched settings differ between two branches, and why."""
from typing import Optional

from .diff_parser import parse_settings
from .gitutil import show_file
from .models import LogEntry


def latest_reason(entries: list[LogEntry], key: str, value: Optional[str]) -> Optional[LogEntry]:
    """The newest log entry that set this exact key to this value."""
    hits = sorted((e for e in entries if e.key == key and e.new == value), key=lambda e: e.created_at)
    return hits[-1] if hits else None


def compare(branch_a: str, branch_b: str, watched: list[str],
            entries: list[LogEntry], cwd: str = ".") -> list[dict]:
    rows = []
    for path in watched:
        a = parse_settings(path, show_file(branch_a, path, cwd=cwd))
        b = parse_settings(path, show_file(branch_b, path, cwd=cwd))
        for key in sorted(set(a) | set(b)):
            if a.get(key) == b.get(key):
                continue
            rows.append({
                "key": key, "file": path,
                "a": a.get(key), "b": b.get(key),
                "why_a": latest_reason(entries, key, a.get(key)),
                "why_b": latest_reason(entries, key, b.get(key)),
            })
    return rows
