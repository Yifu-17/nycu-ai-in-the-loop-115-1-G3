# Evaluation Report (interim, CP2)

Date: 2026-11-23

## What we are trying to show

From our CP1 plan, the tool works if:
1. A teammate can find which setting changed, who changed it, who decided and why, faster and more correctly than with git and chat.
2. Authors accept most AI drafts with small edits instead of rewriting them.

We haven't measured either one yet. This report lists what we have so far and what's still missing.

## Evidence so far

| Evidence | What we did | What we found |
|---|---|---|
| Problem interviews (CP1) | 2 interviews: a course team at NTOU and an NLP lab at NYCU | Both teams lost time finding why a setting changed. One spent two evenings diffing branches, the other about an hour on unsynced environment variables. Both wanted to know who decided, not only who changed it. Their concerns were made-up reasons, the author having to confirm, and sending unpublished research to an outside AI |
| Automated tests | `python -m pytest`, 23 tests, including an end to end test that runs init, log, history and compare on the demo repo | All pass on main, on Mac and on Windows |
| Walking skeleton (11/21) | All four of us connected the real modules and ran the demo after each merge | The main path works end to end. It also showed CLAUDE.md was missing from the drafter PR, fixed in #14 |
| Merge day (11/23) | Merged #18 and #17 one at a time, then a fresh clone on Windows following only the README | Works after fixing two Windows test problems. The README was enough, but it only had Mac commands, so we added Windows ones |
| Week 12 peer review | Group 01 watched our demo | The screen always says "AI draft" even offline (#15). The offline match misses "batch size" with a space. The README didn't explain offline mode (fixed in #23). Strength: the tool says unknown when there's no reason, and shows the sentence the draft came from |
| User tests (11/26) | 2 first-year master's students at NYCU, outside our team, used the tool on our laptop with the demo repo, see design_rationale.md | Both understood the idea and would try it. Both found the CLI hard to use. One asked why a draft was `unknown` before working it out |
| Prompt test suite | 15 cases, 5 typical and 10 edge cases, run on Opus once and Haiku three times | Opus 12/12. Haiku passed the first 12 but added things the input never said, so we added 3 cases. Run 2 failed 2 of them, fixed in CLAUDE.md, run 3 passed 15/15 |

## What we have not tested yet

- The real model on real text. The prompt tests use short commit messages we wrote ourselves. We don't know yet how the AI does on messy real commits and long notes, or how often the evidence check rejects a correct reason.
- Measured results with real users. Our two user tests were short sessions on the demo repo, and we wrote down what testers said, not numbers. We still don't know how many drafts get accepted, edited or rewritten, or whether lookups are faster than with git and chat. We also haven't tested with the two lab teams from CP1 in their own repos.
- Real repos. We have only used our demo repo, where we wrote the commit messages ourselves. Interviewee 1 said their team often writes no reason at all, so on a real repo most drafts might be unknown.
- Environment variables. We watch `.env.example`, but many teams don't commit their real `.env`, so changes there may never reach the tool.
- Two people at once. We expect two people editing log.jsonl to conflict, but we haven't tried it.

## Next steps

1. Run the observation sessions with our two interviewees, using a copy of their own repo if they allow it, and record accept / edit / rewrite for each draft.
2. Update this report with those numbers. Two people is a small sample, so even good results would only be a first sign.
