# Decisions Log

## 2026-09-21 — Initial code steward
Whoever set up the repo (branch protection, PR template, DECISIONS.md) is the initial steward, since they have the most context on the conventions right now.

## 2026-09-21 — AI Usage Guidelines (first draft)

Project: an automation tool that organizes server logs, capturing the reasoning behind parameter changes and team discussions that would otherwise only live in chat.

**Section 1 — Tool-to-task mapping:** We'll use Claude Sonnet to draft summaries of parameter-change discussions into log entries, and Copilot's autocomplete while coding the tool. We won't use AI to decide if a change is safe to deploy, or to write our PR descriptions and DECISIONS.md entries for us.

**Section 2 — Documentation:** Prompts that produce a summary saved as an official log entry get recorded in the prompt engineering log (prompt, model, what we kept vs. edited). If an AI suggestion actually changes our approach, like a different tagging scheme, that goes in DECISIONS.md instead, and the PR description just notes in one line whether AI was involved.

**Section 3 — Disagreements:** If engineers disagree on whether an AI-generated summary is accurate, the code steward decides, based on whether the original author confirms it matches their reasoning, not on seniority or a vote.

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
