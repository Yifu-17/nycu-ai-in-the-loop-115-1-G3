"""STUB: saves the draft without asking. Replaced by the real confirm step."""
from datetime import datetime, timezone

from .models import LogEntry


def make_entry(change, ctx, draft, why, decided_by, status):
    return LogEntry(key=change.key, old=change.old, new=change.new, file=change.file,
                    branch=ctx.branch, commit=ctx.commit, changed_by=ctx.changed_by,
                    decided_by=decided_by, why=why, ai_draft=draft.reason, status=status,
                    created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))


def ask(change, ctx, draft, input_fn=input):
    return make_entry(change, ctx, draft, draft.reason, "(not filled)", "draft")


def auto(change, ctx, draft, decided_by=""):
    return make_entry(change, ctx, draft, draft.reason, decided_by or "(not filled)", "draft")
