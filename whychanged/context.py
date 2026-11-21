"""Collect what people wrote around a change: commit messages, branch, author."""
from .gitutil import git
from .models import ChangeContext


def collect(base: str, head: str, note: str = "", cwd: str = ".") -> ChangeContext:
    messages = git("log", "--format=%B%x00", f"{base}..{head}", cwd=cwd).split("\x00")
    messages = [m.strip() for m in messages if m.strip()]
    branch = git("rev-parse", "--abbrev-ref", head, cwd=cwd).strip()
    if branch == "HEAD":  # detached head or a raw hash was given
        branch = head
    return ChangeContext(
        branch=branch,
        commit=git("rev-parse", "--short", head, cwd=cwd).strip(),
        changed_by=git("log", "-1", "--format=%an", head, cwd=cwd).strip(),
        commit_messages=messages,
        note=note,
    )
