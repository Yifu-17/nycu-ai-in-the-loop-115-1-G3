"""Draft a one-line reason for one setting change.

The system prompt lives in CLAUDE.md at the repo root so it can be read
and reviewed like any other file.

Two safety rules are enforced here in code, not only in the prompt:
1. If the AI's evidence quote is not found in the text we sent, the draft
   is replaced with "unknown". This stops made-up reasons.
2. If there is no API key (or WHYCHANGED_OFFLINE=1), we fall back to a
   simple keyword match so the tool still runs end to end.
"""
import json
import os
from pathlib import Path

from .models import ChangeContext, Draft, SettingChange

PROMPT_FILE = Path(__file__).resolve().parent.parent / "CLAUDE.md"
MODEL = os.environ.get("WHYCHANGED_MODEL", "claude-opus-5-5")

SCHEMA = {
    "type": "object",
    "properties": {
        "reason": {"type": "string"},
        "evidence": {"type": "string"},
    },
    "required": ["reason", "evidence"],
    "additionalProperties": False,
}


def build_input(change: SettingChange, ctx: ChangeContext) -> str:
    messages = "\n---\n".join(ctx.commit_messages) or "(none)"
    return (
        f"<change>\n{change.key}: {change.old} -> {change.new} ({change.file})\n</change>\n"
        f"<commit_messages>\n{messages}\n</commit_messages>\n"
        f"<note>\n{ctx.note or '(none)'}\n</note>"
    )


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def evidence_is_real(evidence: str, change: SettingChange, ctx: ChangeContext) -> bool:
    if not evidence.strip():
        return False
    source = _normalize(" ".join(ctx.commit_messages) + " " + ctx.note)
    return _normalize(evidence) in source


def offline_draft(change: SettingChange, ctx: ChangeContext) -> Draft:
    """Without AI: use the first commit line or note line that names the setting."""
    last_part = change.key.split(".")[-1].lower()
    lines = []
    for text in ctx.commit_messages + [ctx.note]:
        lines.extend(line.strip() for line in text.splitlines() if line.strip())
    for line in lines:
        if last_part in line.lower():
            return Draft(reason=line, evidence=line, source="offline")
    return Draft(reason="unknown", evidence="", source="offline")


def ai_draft(change: SettingChange, ctx: ChangeContext) -> Draft:
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=PROMPT_FILE.read_text(encoding="utf-8"),
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": build_input(change, ctx)}],
    )
    if response.stop_reason == "refusal":
        return Draft(reason="unknown", evidence="", source="error")
    text = next(b.text for b in response.content if b.type == "text")
    data = json.loads(text)
    reason = data["reason"].strip().splitlines()[0] if data["reason"].strip() else "unknown"
    evidence = data["evidence"].strip()
    if reason.lower() != "unknown" and not evidence_is_real(evidence, change, ctx):
        return Draft(reason="unknown", evidence="", source="ai")
    return Draft(reason=reason, evidence=evidence, source="ai")


def draft_reason(change: SettingChange, ctx: ChangeContext) -> Draft:
    if os.environ.get("WHYCHANGED_OFFLINE") == "1" or not os.environ.get("ANTHROPIC_API_KEY"):
        return offline_draft(change, ctx)
    try:
        return ai_draft(change, ctx)
    except Exception as exc:  # network, quota, bad JSON: never block the author
        print(f"[whychanged] AI draft failed ({type(exc).__name__}), using offline draft")
        return offline_draft(change, ctx)
