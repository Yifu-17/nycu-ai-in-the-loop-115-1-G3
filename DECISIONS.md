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


## 2026-10-19 — Current code steward: 陳繹夫 (@Yifu-17)
Decision: 陳繹夫 (@Yifu-17) is the current code steward.
Why: they own the repository and set up branch protection, the PR template and DECISIONS.md, so they already hold the most context on our conventions. This replaces the unnamed "whoever set up the repo" entry above.
Rotation: the steward changes weekly in the order 陳繹夫 → 吳傢澂 → 吳承霖 → 楊敦傑, so everyone serves once before CP2 and twice before CP3. Only the steward approves and merges PRs to main; when the steward authors a PR, the next steward reviews it. Each handover gets its own entry here.
Alternative rejected: two-week terms, which would leave some members serving only once by CP3.
Led by: 吳傢澂

## 2026-10-19 — Evaluation plan revised for CP1 (replaces the 2026-09-21 draft)
Decision: evaluate with 3 pairs of people outside our team (3 authors, 3 readers) in a structured observation in Weeks 13–14, instead of interviewing our own team.
Why: the CP1 rubric requires target users outside the team, and "one real case with minor edits" would not convince a skeptic. The new plan measures what changes for users: whether readers find the correct reason faster than with chat search (at least 2 of 3), and whether authors accept AI drafts with minor edits (at least 9 of 12). Full plan is in Group03_CP1.md, section 4.
Alternative rejected: testing only with our own team. We make and explain the changes ourselves, so we would be evaluating our own habits instead of a real user's.
Led by: 吳傢澂
