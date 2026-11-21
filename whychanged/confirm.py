"""Show the AI draft to the author and turn it into a log entry.

The author can accept the draft, type a new reason, or skip.
"Decided by" is always typed by a person; the AI never fills it.
"""
from datetime import datetime, timezone
from typing import Callable, Optional

from .models import ChangeContext, Draft, LogEntry, SettingChange


def make_entry(change: SettingChange, ctx: ChangeContext, draft: Draft,
               why: str, decided_by: str, status: str) -> LogEntry:
    return LogEntry(
        key=change.key, old=change.old, new=change.new, file=change.file,
        branch=ctx.branch, commit=ctx.commit, changed_by=ctx.changed_by,
        decided_by=decided_by, why=why, ai_draft=draft.reason, status=status,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def ask(change: SettingChange, ctx: ChangeContext, draft: Draft,
        input_fn: Callable[[str], str] = input) -> Optional[LogEntry]:
    print(f"\n{change.key}: {change.old} -> {change.new}  ({change.file})")
    print(f"  AI draft: {draft.reason}")
    if draft.evidence:
        print(f"  based on: \"{draft.evidence}\"")
    choice = input_fn("  [a]ccept / [e]dit / [s]kip > ").strip().lower()
    if choice.startswith("s"):
        return None
    why = draft.reason
    if choice.startswith("e") or why == "unknown":
        typed = input_fn("  why did this change? > ").strip()
        why = typed or why
    decided_by = input_fn("  who decided? > ").strip()
    status = "confirmed" if decided_by and why != "unknown" else "draft"
    return make_entry(change, ctx, draft, why, decided_by or "(not filled)", status)


def auto(change: SettingChange, ctx: ChangeContext, draft: Draft,
         decided_by: str = "") -> LogEntry:
    """Non-interactive: save the draft as-is with status draft (for CI or scripts)."""
    return make_entry(change, ctx, draft, draft.reason, decided_by or "(not filled)", "draft")
