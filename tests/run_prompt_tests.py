"""Run the prompt test suite against the real model and save the results.

  ANTHROPIC_API_KEY=... python tests/run_prompt_tests.py [--out tests/results/run1.md]

This calls the API once per case (12 calls). It does not run under pytest.
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from whychanged.drafter import MODEL, ai_draft  # noqa: E402
from whychanged.models import ChangeContext, SettingChange  # noqa: E402

CASES = Path(__file__).with_name("prompt_cases.yaml")


def check(case: dict, reason: str) -> tuple[bool, str]:
    low = reason.lower()
    if case["expect"] == "unknown" and low != "unknown":
        return False, "expected unknown"
    if case["expect"] == "grounded" and low == "unknown":
        return False, "expected a grounded reason"
    for w in case.get("must_include", []):
        if w.lower() not in low:
            return False, f"missing '{w}'"
    for w in case.get("must_not_include", []):
        if w.lower() in low:
            return False, f"contains '{w}'"
    return True, ""


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=f"tests/results/{date.today()}.md")
    args = p.parse_args()

    rows, passed = [], 0
    for case in yaml.safe_load(CASES.read_text(encoding="utf-8")):
        change = SettingChange(**case["change"])
        ctx = ChangeContext(branch="test", commit="0000000", changed_by="tester",
                            commit_messages=case.get("commits", []), note=case.get("note", ""))
        draft = ai_draft(change, ctx)
        ok, why = check(case, draft.reason)
        passed += ok
        rows.append(f"| {case['id']} | {case['type']} | {draft.reason} | {'PASS' if ok else 'FAIL ' + why} |")
        print(rows[-1])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"# Prompt test run {date.today()}\n\nModel: {MODEL}\n\nPassed {passed}/{len(rows)}\n\n"
        "| Case | Type | Reason | Result |\n|---|---|---|---|\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )
    print(f"\nPassed {passed}/{len(rows)}. Saved to {out}")


if __name__ == "__main__":
    main()
