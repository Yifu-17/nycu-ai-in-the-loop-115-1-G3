"""Find which settings changed between two revisions. Plain code, no AI.

Instead of reading the text diff, we load the settings file at both
revisions, flatten each into {key: value}, and compare the two dicts.
This way reordering lines or changing comments does not count as a change.
"""
import json
from typing import Optional

import yaml

from .gitutil import show_file, changed_files
from .models import SettingChange


def flatten(data, prefix: str = "") -> dict[str, str]:
    """{"train": {"lr": 0.001}} -> {"train.lr": "0.001"}"""
    out: dict[str, str] = {}
    if isinstance(data, dict):
        for k, v in data.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out.update(flatten(v, key))
    elif isinstance(data, list):
        out[prefix] = json.dumps(data, ensure_ascii=False)
    else:
        out[prefix] = "null" if data is None else str(data)
    return out


def parse_env(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        key, _, value = line.partition("=")
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def parse_settings(path: str, text: Optional[str]) -> dict[str, str]:
    if text is None:
        return {}
    name = path.lower()
    if name.endswith((".yaml", ".yml")):
        return flatten(yaml.safe_load(text) or {})
    if name.endswith(".json"):
        return flatten(json.loads(text or "{}"))
    if ".env" in name.rsplit("/", 1)[-1]:
        return parse_env(text)
    raise ValueError(f"unsupported settings file: {path}")


def compare_dicts(before: dict, after: dict, file: str) -> list[SettingChange]:
    changes = []
    for key in sorted(set(before) | set(after)):
        old, new = before.get(key), after.get(key)
        if old != new:
            changes.append(SettingChange(key=key, old=old, new=new, file=file))
    return changes


def find_changes(base: str, head: str, watched: list[str], cwd: str = ".") -> list[SettingChange]:
    """All setting changes in watched files between base and head."""
    touched = set(changed_files(base, head, cwd=cwd))
    changes: list[SettingChange] = []
    for path in watched:
        if path not in touched:
            continue
        before = parse_settings(path, show_file(base, path, cwd=cwd))
        after = parse_settings(path, show_file(head, path, cwd=cwd))
        changes.extend(compare_dicts(before, after, path))
    return changes
