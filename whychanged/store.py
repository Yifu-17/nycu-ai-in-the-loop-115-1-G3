"""Save and load log entries. One JSON object per line in .whychanged/log.jsonl.

The log file is committed to the repo, so everyone on the team sees it.
"""
import json
from pathlib import Path

from .models import LogEntry

LOG_DIR = ".whychanged"
LOG_FILE = "log.jsonl"


def log_path(repo: str = ".") -> Path:
    return Path(repo) / LOG_DIR / LOG_FILE


def append(entries: list[LogEntry], repo: str = ".") -> Path:
    path = log_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")
    return path


def load(repo: str = ".") -> list[LogEntry]:
    path = log_path(repo)
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(LogEntry.from_dict(json.loads(line)))
    return entries
