# whychanged

Records why shared experiment settings changed, and who decided.

When someone changes a watched settings file (e.g. `configs/train.yaml`, `.env.example`), whychanged lists each changed setting, drafts a one-line reason from the commit messages with Claude, and asks the author to confirm it and fill in who decided. Weeks later, anyone can look up a setting's history or compare two branches.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...   # optional; without it the tool uses a simple offline draft
```

Without a key, or with `WHYCHANGED_OFFLINE=1`, the tool runs in offline mode. It doesn't call any AI. For each changed setting it takes the first line in the commit messages or the note that mentions the setting's name, for example `dropout` for `train.dropout`, and uses that line as the draft. If no line mentions it, the draft is `unknown`. Offline drafts are a rough match, so check them more carefully before you accept. If the AI call fails, the tool also falls back to offline mode and prints a message.

## Try it on the demo repo (2 people)

```bash
bash demo/make_demo_repo.sh /tmp/demo-lab

# Person A changed dropout and batch size on feat/head-dropout
python -m whychanged --repo /tmp/demo-lab init --watch configs/train.yaml .env.example
python -m whychanged --repo /tmp/demo-lab log --base main --markdown
#   -> confirm or edit each draft, type who decided, paste the table into the PR

# Person B, weeks later
python -m whychanged --repo /tmp/demo-lab history dropout
python -m whychanged --repo /tmp/demo-lab compare feat/head-dropout exp/old-lr
```

## Commands

| Command | What it does |
|---|---|
| `init --watch FILE...` | Choose which settings files to watch (saved in `.whychanged/config.yaml`) |
| `log --base main [--head HEAD] [--note-file F] [--yes] [--markdown]` | Draft reasons for changed settings, ask the author, save to `.whychanged/log.jsonl` |
| `history KEY` | Every logged change of one setting (`train.lr` or just `lr`) |
| `compare A B` | Settings that differ between two branches, with the logged reasons |

## How it works

```
git diff ─> diff_parser ─> context ─> drafter (Claude) ─> confirm ─> store ─> history / compare
            which keys     commit msgs  one-line reason    author     log.jsonl
            changed        + PR note    or "unknown"       decides
```

- `diff_parser` and `context` are plain code. The AI never decides what changed.
- `drafter` uses the system prompt in [CLAUDE.md](CLAUDE.md). If the AI's quoted evidence is not in the input, the draft becomes "unknown".
- "Decided by" is always typed by a person.

## Tests

```bash
pytest                                  # unit + end-to-end, offline
python tests/run_prompt_tests.py        # prompt test suite, calls the API (12 cases)
```
