"""STUB: keeps entries in memory only. Replaced by the real jsonl store."""
from pathlib import Path

LOG_DIR = ".whychanged"
_MEMORY = []


def append(entries, repo="."):
    _MEMORY.extend(entries)
    return Path(repo) / LOG_DIR / "(in memory)"


def load(repo="."):
    return list(_MEMORY)
