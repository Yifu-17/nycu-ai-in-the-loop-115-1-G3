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
