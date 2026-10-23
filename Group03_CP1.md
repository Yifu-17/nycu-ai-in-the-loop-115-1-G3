# Group 03 — Checkpoint 1

Team: 陳繹夫, 吳傢澂, 吳承霖, 楊敦傑

## 1. Team Charter

### Decisions when we disagree
1. Each person posts their view in the LINE group. Everyone replies within 24 hours.
2. If we still don't agree, the "Led by" person of that work decides.
3. If the Led by person is part of the disagreement, the current code steward decides. If the steward is also involved, the next steward decides.
4. If all four are involved, we vote. On a 2–2 tie we keep what is on `main` and ask the TA.
5. The result goes into DECISIONS.md.

### Definition of done
- Merged into `main` through a PR (branch protection blocks direct pushes).
- Approved and merged by the code steward with at least one review comment. If the steward wrote the PR, the next steward reviews it.
- PR description follows the template.
- If it changes our approach, there is a DECISIONS.md entry.
- For code: someone other than the author has run it once.

### Code steward rotation
Changes every week starting Week 7, in this order: 陳繹夫 → 吳傢澂 → 吳承霖 → 楊敦傑. Everyone is steward once before CP2 and twice before CP3.

### Communication outside class
- Channel: LINE group for daily talk, GitHub PRs and issues for code.
- Frequency: meeting every Friday 21:00–22:00.
- Response time: within 24 hours on weekdays and 48 hours on weekends. Within 12 hours in the 3 days before a checkpoint.

## 2. Problem Statement with Evidence

### The problem
In research teams that share one GitHub repo, members often change shared experiment settings, such as learning rate, batch size, dropout, or environment variables. Git shows that a file changed, but not why, or who decided it. Commit messages are usually just "update model" or "fix", and reasons, if written at all, get buried in LINE.

This becomes a problem when results don't match, for example an old branch scores higher than `main`, or two people run the same experiment and get different numbers. Then someone has to diff branches and ask everyone "did you change this?".

The people affected are the member trying to find out why results changed, and the member who made the change and gets asked about it weeks later.

### Evidence from real users

**Interviewee 1: master's student at NTOU, 4-person course team (protein recognition model)**
- The team shares one repo and one training config. Each person owns a part (data, model, training, evaluation), but it all runs as one model.
- They change settings almost every week, and 2–3 times a day before a report is due, often on different branches at the same time.
- About 3 weeks ago, an old branch scored almost 3 points higher in validation accuracy than `main`. The commits only said "update model" / "fix". They spent two evenings diffing branches and messaging each person, still couldn't find the cause, and had to rerun experiments less than a week before the deadline.
- They tried LINE messages and a shared Google Doc / Notion page, but messages get buried and nobody updates the doc when busy.
- On an AI-written log, they worried that the AI would make up a reason, that the author must confirm it, that unpublished research might be sent to an outside AI, and that fixing a long AI paragraph would take longer than writing one line.

**Interviewee 2: graduate student in an NLP lab at NYCU, 7 members**
- The lab shares one repo and changes environment variables about once a week, since everyone needs the same environment.
- Members once ran the same experiment and got different results. The cause was environment variables that hadn't been synced, and finding it took about one hour.
- They keep a `rule.md` file for settings, but it doesn't show who changed a rule or who decided it.
- They would use a tool like this, and are fine with it reading team chat, as long as it records who made the change and who decided it.

### Why existing tools don't solve it
- Git commits and diffs: show what changed and who committed, but not why or who decided. Interviewee 1 diffed branches for two evenings and still couldn't find the cause.
- LINE: messages like "I changed dropout to 0.3" get buried and aren't linked to a branch.
- Google Doc / Notion / `rule.md`: Interviewee 1's team stops updating the doc when busy. Interviewee 2's `rule.md` has no record of who changed or decided a rule.

## 3. Initial Interaction Design Sketch

### What the tool does
When a commit or PR changes a shared settings file, the tool lists the changed settings, uses AI to draft a one-line reason, and asks the author to confirm it and say who decided.

### Inputs and outputs
Inputs:
- The diff of settings files the team lists (e.g. `configs/train.yaml`, `.env.example`). Read by normal code, not AI.
- The commit message and PR description. Team chat only if the team opts in.
- The author's reply: who decided, and a fixed reason if the draft is wrong.

Outputs:
- One entry per changed setting, saved in the repo and posted on the PR:

```
lr: 1e-3 -> 5e-4  (configs/train.yaml)
Branch/commit: feat/head-dropout @ a1b2c3d
Changed by:    <from git>
Decided by:    <filled in by the author>
Why:           <AI draft, confirmed or edited by the author>
Status:        draft / confirmed
```

- A lookup: search a setting's history, or compare two branches to see which settings differ and why.

### How two people use it
1. A changes `configs/train.yaml` and opens a PR.
2. The tool drafts the reason and asks A to confirm it and fill in who decided.
3. A confirms or edits it, and the entry is posted on the PR.
4. B (e.g. the reviewer) sees the reason while reviewing.
5. Weeks later, B compares `main` with an old branch and sees each changed setting with its reason, instead of asking everyone.

## 4. Draft Evaluation Plan

### Success definition
We will know our tool works if:
- A teammate can find which setting changed, who changed it, who decided, and why faster and more correctly with the tool than with git and chat.
- Authors accept most AI drafts with small edits instead of rewriting them.

### Target users and access
Our two interviewees (NTOU course team and NYCU NLP lab). We already have contact with both.

### Method and timing
Structured observation in Weeks 13–14, about 30 minutes with each interviewee:
1. Each person makes 4 setting changes in a copy of their own repo and reviews the tool's drafts. We count how many drafts they accept, edit, or rewrite.
2. Each person then looks up the other person's 4 changes, 2 with git and chat only and 2 with the tool. We record time and correctness.
3. A short interview afterward.

### Minimum evidence threshold
- Both people get all tool-assisted lookups fully correct, and are faster on average with the tool than with git and chat.
- At least 6 of the 8 AI drafts are accepted with small edits or none.

Two people is a small sample, so even if this works, we would still need to test with more teams.

### Human-AI boundary
- Code (not AI): which settings changed and who committed them.
- AI: drafts the reason.
- Human: confirms the reason, fills in who decided (the AI never guesses this), and decides whether to keep the change.
- The AI never changes settings or merges PRs.

### What we're unsure about
- Interviewee 1's team often writes no reason at all, so the AI may have little to work with.
- `.env` files are often not committed, so we may need another way to track environment variables.
- Labs may not allow sending diffs to an outside AI.

## 5. Repository

- Link: https://github.com/Yifu-17/nycu-ai-in-the-loop-115-1-G3
- Branch protection on `main`: enabled
- PR template: `.github/PULL_REQUEST_TEMPLATE.md`
- DECISIONS.md: started, with 6 entries
- Current code steward: 陳繹夫 (@Yifu-17), recorded in DECISIONS.md
