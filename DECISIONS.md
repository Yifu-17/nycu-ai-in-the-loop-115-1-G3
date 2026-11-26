# Decisions Log

## 2026-09-21 — Initial code steward
Whoever set up the repo (branch protection, PR template, DECISIONS.md) is the initial steward, since they have the most context on the conventions right now.

## 2026-09-21 — AI Usage Guidelines (first draft)

Project: an automation tool that organizes server logs, capturing the reasoning behind parameter changes and team discussions that would otherwise only live in chat.

**Section 1 — Tool-to-task mapping:** We'll use Claude Sonnet to draft summaries of parameter-change discussions into log entries, and Copilot's autocomplete while coding the tool. We won't use AI to decide if a change is safe to deploy, or to write our PR descriptions and DECISIONS.md entries for us.

**Section 2 — Documentation:** Prompts that produce a summary saved as an official log entry get recorded in the prompt engineering log (prompt, model, what we kept vs. edited). If an AI suggestion actually changes our approach, like a different tagging scheme, that goes in DECISIONS.md instead, and the PR description just notes in one line whether AI was involved.

**Section 3 — Disagreements:** If engineers disagree on whether an AI-generated summary is accurate, the code steward decides, based on whether the original author confirms it matches their reasoning, not on seniority or a vote.

## 2026-11-23 — AI Usage Guidelines (updated from CP2)
We looked at PRs #10 to #20: AI wrote most of the code in all 10, someone other than the author could explain all 10, and 0 of 10 said what the AI did. So we changed three rules from the first draft above.
1. Old: we won't use AI to write our PR descriptions and DECISIONS.md entries. New: AI can draft code and PR text, but every PR needs a reviewer comment that the author answers in their own words before it's approved. Why: in CP2 AI wrote most of it, and what made it work was that everyone read it, reviewed someone else's PR and connected the pieces.
2. Old: the PR description notes in one line whether AI was involved. New: every PR fills in the AI assistance section of the PR template, and a PR with it empty doesn't get approved. Why: none of our 10 PRs said what the AI did, and Group 01 pointed this out in the Week 12 review.
3. Old: prompts that produce an official log entry go in the prompt engineering log. New: a PR that changes the AI's behavior includes CLAUDE.md and the prompt test results from before and after. Why: #12 changed the drafter but left CLAUDE.md out, and it had to be added later in #14.
Led by: 陳繹夫

## 2026-09-21 — Draft Evaluation Plan

**Problem grounding:**
- Who: the teammate who changes a parameter on our shared server and explains why in the group chat.
- What they do now: the explanation stays buried in chat history, so later someone has to scroll back or ask the author directly.
- What changes: that explanation gets attached to the change itself as a log entry, so anyone can find it without asking.

**Evaluation plan:**
- Success definition: a sample of recent parameter changes each has a log entry the original author confirms matches their reasoning. The AI drafts the summary and a human reviews it before it's saved, so success is about the draft being accurate enough that review stays quick, not about the AI deciding on its own.
- Target users: our own team, since we're also the ones making and explaining these changes on the server.
- Method: a short interview with the author right after the tool logs their change, asking if the summary is right. Planned around the CP1 checkpoint.
- Minimum evidence threshold: one real case where the tool's summary needed only minor edits, not a rewrite.

## 2026-10-19 — Current code steward: 陳繹夫
Rotation: the steward changes weekly in the order 陳繹夫 → 吳傢澂 → 吳承霖 → 楊敦傑, so everyone serves once before CP2 and twice before CP3. Only the steward approves and merges PRs to main; when the steward authors a PR, the next steward reviews it. Each handover gets its own entry here.
Led by: 吳傢澂

## 2026-10-22 — Problem scope changed to shared experiment settings
Decision: the tool tracks changes to training configs and environment variables in a research team's shared repo, instead of parameters on a shared server.
Why: both interviewees (a course team at NTOU and an NLP lab at NYCU) had this problem, not the server one. What they couldn't find later was why a setting changed and who decided it.
Led by: 吳傢澂

## 2026-10-22 — Evaluation plan revised for CP1
Decision: in Weeks 13–14, test the tool with our 2 interviewees instead of our own team.
Why: CP1 requires testing with people outside the team, and both interviewees already have this problem in their own repos.
Led by: 吳傢澂

## 2026-11-20 — Prototype is a Python CLI
Decision: build the tool as a Python command line tool that runs inside the team's repo. Commands: `log` drafts and confirms reasons, `history` shows one setting's changes, `compare` shows settings that differ between two branches.
Why: it runs on any laptop, so we can demo it in the Week 12 lab and use it in user tests without setting up CI. A table for the PR can be printed from the same code.
Alternative rejected: a GitHub Action that comments on PRs, since it needs repo secrets and CI before anything runs.
Led by: 陳繹夫

## 2026-11-20 — CP2 work split
Decision: the pipeline is split into modules with fixed hand-offs in `whychanged/models.py`. 陳繹夫 builds the skeleton with stub modules, then each person replaces stubs with real code.
- 吳傢澂: settings diff parser, branch compare
- 吳承霖: AI drafter and CLAUDE.md, prompt test suite
- 楊敦傑: confirm step and log store, setting history
- 陳繹夫: skeleton, PR output and README
Why: each module can be built and reviewed on its own branch, and the skeleton runs end to end before any real module is in.
Led by: 陳繹夫

## 2026-11-21 — Steward is the next person after the author
Decision: from CP2 on, each PR's steward is the next person after its author in the order 陳繹夫 → 吳傢澂 → 吳承霖 → 楊敦傑 → 陳繹夫. That person comments on the PR, waits for the author's reply, then approves and merges.
Why: most PRs land around the two team sessions, so a weekly steward would review almost all of them alone. Tying the steward to the PR spreads reviews evenly, and everyone is steward before CP2.
Led by: 陳繹夫

## 2026-11-21 — Walking skeleton
Decision: kept the stubs from #10 so the whole path ran before any real code, then swapped in diff_parser, drafter and confirm/store one PR at a time (#11 to #14). history and compare stay stubs until the next slice.
Why: every PR could be reviewed and merged on its own, and we could run the demo after each merge to see which piece broke.
Led by: 陳繹夫

## 2026-11-21 — Steward record for CP2
Each PR's steward commented, waited for the author's reply, then approved.
- #10 skeleton by 陳繹夫, steward 吳傢澂
- #11 diff_parser by 吳傢澂, steward 吳承霖
- #12 drafter by 吳承霖, steward 楊敦傑
- #13 confirm and store by 楊敦傑, steward 陳繹夫
- #14 CLAUDE.md by 吳承霖, steward 楊敦傑
- #16 markdown table and README by 陳繹夫, steward 吳傢澂
Led by: 陳繹夫

## 2026-11-23 — Merge plan for merge day
Open PRs:
- #18 `jcwu/compare` by 吳傢澂: compare two branches with logged reasons. Ready. Only touches compare.py and its test.
- #17 `tcyang/history` by 楊敦傑: setting history and an end to end test. Ready, but its end to end test needs compare, so it only passes after #18 compare is merged. Only touches history.py and its tests.
- #19 `clwu/prompt-tests` by 吳承霖: 12 prompt test cases and the runner. Ready only if it has real API results. Only touches files in tests/.

Order: #18 compare, then #17 history, then #19 prompt-tests. history's end to end test runs compare, so compare goes first. prompt-tests only adds test files and is last because it depends on the API key.
Conflicts we expect: none, the three PRs don't touch the same files.
Done means: on a fresh clone of main, pytest passes and log, history and compare all give real output on the demo repo.
Closing without merging: none.
Led by: 陳繹夫

Outcome (2026-11-23): merged #18 and #17. #19 is left open until we get the API key. No conflicts. The tests failed on Windows at first: bare `pytest` couldn't import whychanged, and the tests called `bash`, which on Windows runs WSL bash. Fixed in #18 (6d38a5b) and #17 by adding `pythonpath = .` to pytest.ini and using the bash that ships with git. Fresh-clone test by 吳承霖 on Windows: worked, we only added Windows commands to the README. main is green, 23 passed. Left for later: #19, issues #15, #21.

## 2026-11-26 — Drafter uses Haiku, and two prompt rules from a failed test
Decision: the drafter's default model is now `claude-haiku-5-5` instead of `claude-opus-5-5`.
Why: our API budget is $5 until the end of term. Each draft is one short call, and on the first run Haiku passed the same 12 prompt tests as Opus.
Alternative rejected: keeping Opus. It also passed 12/12, but costs more for a one-line reason.

Haiku passed 12/12 but still wrote "as advised" for E06 and added "to reduce overfitting" for E07, which the input never said. We added E08 to E10 to catch this, and run 2 failed E08 and E09 (13/15). We added two rules to CLAUDE.md: don't add a purpose the text doesn't state, and don't say who suggested or advised the change. Run 3 passed 15/15. Results are in tests/results/.
Led by: 陳繹夫
