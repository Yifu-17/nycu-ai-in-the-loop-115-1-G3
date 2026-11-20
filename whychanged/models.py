"""Data shapes passed between the pipeline steps.

diff_parser -> list[SettingChange]
context     -> ChangeContext
drafter     -> Draft
confirm     -> LogEntry (saved by store)
"""
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class SettingChange:
    key: str                # dotted path, e.g. "train.lr" or "CUDA_VISIBLE_DEVICES"
    old: Optional[str]      # None if the setting was added
    new: Optional[str]      # None if the setting was removed
    file: str               # e.g. "configs/train.yaml"


@dataclass
class ChangeContext:
    branch: str
    commit: str             # short hash of the head commit
    changed_by: str         # git author name of the head commit
    commit_messages: list[str] = field(default_factory=list)
    note: str = ""          # PR description or chat text the author chose to paste


@dataclass
class Draft:
    reason: str             # one line, or "unknown" when there is no evidence
    evidence: str           # the exact text the reason came from, "" if unknown
    source: str             # "ai", "offline", or "error"


@dataclass
class LogEntry:
    key: str
    old: Optional[str]
    new: Optional[str]
    file: str
    branch: str
    commit: str
    changed_by: str
    decided_by: str
    why: str
    ai_draft: str
    status: str             # "draft" or "confirmed"
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "LogEntry":
        return cls(**{k: d.get(k) for k in cls.__dataclass_fields__})
