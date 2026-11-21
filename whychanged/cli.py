"""Command line entry point.

  python -m whychanged init  --watch configs/train.yaml .env.example
  python -m whychanged log   --base main [--head HEAD] [--note-file pr.txt] [--yes]
  python -m whychanged history train.lr
  python -m whychanged compare main old-branch
"""
import argparse
import sys
from pathlib import Path

import yaml

from . import compare, confirm, context, diff_parser, drafter, history, store

CONFIG = Path(store.LOG_DIR) / "config.yaml"


def load_watched(repo: str) -> list[str]:
    path = Path(repo) / CONFIG
    if not path.exists():
        sys.exit("No .whychanged/config.yaml. Run `python -m whychanged init --watch <files>` first.")
    return (yaml.safe_load(path.read_text()) or {}).get("watch", [])


def cmd_init(args) -> None:
    path = Path(args.repo) / CONFIG
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"watch": args.watch}, allow_unicode=True))
    print(f"Watching {len(args.watch)} file(s). Saved to {path}")


def cell(text) -> str:
    # a | or a line break inside a cell breaks the markdown table
    return str(text).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def as_markdown(entries) -> str:
    lines = ["| Setting | Change | Why | Decided by | Status |", "|---|---|---|---|---|"]
    for e in entries:
        lines.append(f"| `{cell(e.key)}` | {cell(e.old)} → {cell(e.new)} | {cell(e.why)} "
                     f"| {cell(e.decided_by)} | {cell(e.status)} |")
    return "\n".join(lines)


def cmd_log(args) -> None:
    watched = load_watched(args.repo)
    changes = diff_parser.find_changes(args.base, args.head, watched, cwd=args.repo)
    if not changes:
        print("No watched settings changed.")
        return
    note = Path(args.note_file).read_text(encoding="utf-8") if args.note_file else ""
    ctx = context.collect(args.base, args.head, note=note, cwd=args.repo)
    entries = []
    for change in changes:
        draft = drafter.draft_reason(change, ctx)
        if args.yes:
            entries.append(confirm.auto(change, ctx, draft, args.decided_by))
        else:
            entry = confirm.ask(change, ctx, draft)
            if entry:
                entries.append(entry)
    if not entries:
        print("Nothing saved.")
        return
    path = store.append(entries, repo=args.repo)
    print(f"\nSaved {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} to {path}")
    if args.markdown:
        print("\n" + as_markdown(entries))


def cmd_history(args) -> None:
    hits = history.history(store.load(args.repo), args.key)
    if not hits:
        print(f"No log entries for {args.key}.")
        return
    for e in hits:
        print(f"{e.created_at[:10]}  {e.key}: {e.old} -> {e.new}  [{e.status}]")
        print(f"    why:        {e.why}")
        print(f"    changed by: {e.changed_by}   decided by: {e.decided_by}")
        print(f"    where:      {e.branch} @ {e.commit} ({e.file})")


def cmd_compare(args) -> None:
    rows = compare.compare(args.a, args.b, load_watched(args.repo), store.load(args.repo), cwd=args.repo)
    if not rows:
        print(f"No watched settings differ between {args.a} and {args.b}.")
        return
    for r in rows:
        print(f"{r['key']}  ({r['file']})")
        for side, value, why in ((args.a, r["a"], r["why_a"]), (args.b, r["b"], r["why_b"])):
            reason = f"{why.why}  (decided by {why.decided_by})" if why else "no log entry"
            print(f"    {side:<20} {value!s:<12} {reason}")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="whychanged", description="Record why shared settings changed.")
    p.add_argument("--repo", default=".", help="path to the git repo (default: current folder)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="choose which settings files to watch")
    s.add_argument("--watch", nargs="+", required=True)
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("log", help="draft and confirm reasons for changed settings")
    s.add_argument("--base", default="main")
    s.add_argument("--head", default="HEAD")
    s.add_argument("--note-file", help="text file with the PR description or chat message")
    s.add_argument("--yes", action="store_true", help="save drafts without asking")
    s.add_argument("--decided-by", default="")
    s.add_argument("--markdown", action="store_true", help="also print a table to paste into the PR")
    s.set_defaults(func=cmd_log)

    s = sub.add_parser("history", help="show every logged change of one setting")
    s.add_argument("key")
    s.set_defaults(func=cmd_history)

    s = sub.add_parser("compare", help="settings that differ between two branches, with reasons")
    s.add_argument("a")
    s.add_argument("b")
    s.set_defaults(func=cmd_compare)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
