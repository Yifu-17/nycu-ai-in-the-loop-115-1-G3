# Design Rationale (CP2)

whychanged helps a research team that shares one GitHub repo find out why an experiment setting changed and who decided it. When someone changes a watched settings file, AI drafts a one-line reason from the commit messages, and the author confirms it and types who decided.

This page lists our main design decisions, what shaped each one, and what our two user tests showed.

## What shaped the design

- Two problem interviews in CP1, with a course team at NTOU and an NLP lab at NYCU. Both lost hours finding why a setting changed. Both wanted to know who decided, not only who changed it. They worried about AI making up reasons and about sending unpublished research to an outside AI.
- Group 01's review of our demo in the Week 12 lab.
- Our prompt tests, 15 cases on Opus and Haiku.
- Two user tests on 2026-11-26, below.

## Main decisions

| Decision | Why | What we rejected |
|---|---|---|
| A Python CLI that runs in the team's repo | Runs on any laptop, no CI or repo secrets needed, easy to demo and test | A GitHub Action that comments on PRs, since it needs secrets and CI before anything runs |
| Plain code finds what changed, AI only drafts the reason | Which setting changed and who committed it are facts in git. The AI shouldn't be able to get them wrong | Letting the AI read the whole diff and summarize it |
| The AI says `unknown` instead of guessing | Both interviewees worried about made-up reasons. A wrong reason is worse than none, because people trust it weeks later | Filling in a common reason, like "lower lr for stability" |
| Every draft shows the sentence it came from, and code checks that the sentence is really in the input | The author can check a draft in a second, and a made-up quote becomes `unknown` | Trusting the AI's output as is |
| "Who decided" is always typed by a person | That's the part git can't tell you, and both interviewees asked for it. The AI can't know it from commit text | Letting the AI read it from the text, like "advisor said". Our prompt test E09 now checks the AI doesn't do this |
| One question per setting, accept / edit / skip | A long AI paragraph takes longer to fix than writing one line, which interviewee 1 told us | One summary of the whole PR |
| A table printed for the PR description | Reviewers can see the reasons without installing the tool | Only saving to log.jsonl |
| Offline mode without a key | The tool still runs end to end for anyone, and nothing is sent outside | Requiring a key to run at all |
| Haiku as the default model | Our budget is $5 until the end of term, and Haiku passed the same prompt tests after two prompt fixes | Opus, which also passed but costs more for a one-line reason |

## User tests

Two first-year master's students at NYCU, outside our team, on 2026-11-26. Each test was about 20 minutes on our laptop with the demo repo and the real AI drafter. They typed the commands themselves. Task 1: log the reasons for two changed settings as the author. Task 2: weeks later, find why settings differ between two branches using `history` and `compare`.

| | Tester 1 | Tester 2 |
|---|---|---|
| What they asked or got stuck on | Asked why the batch_size draft was `unknown`, then worked out it was because the commit message didn't mention it | Found the commands a bit complicated |
| What they liked | "Pretty cool", would like to try it | Likes the idea, would like to try it |
| What they'd change | Not used to the CLI | Wrap it into one tool or give it a UI |

What we learned:

1. The idea works for people outside our team. Both understood the problem and would try it.
2. `unknown` was right, but the screen didn't say why. Tester 1 had to work it out. The screen should say something like "no commit message mentions batch_size".
3. The CLI is the biggest barrier. Both testers found the commands hard, which matches the trade-off we made when we chose a CLI. The long commands with `--repo`, `--base` and `--markdown` are the problem, not the idea.

## What we will change in Phase 3

- Show why a draft is `unknown`, and whether it came from the AI or the offline version (#15).
- Make the commands shorter: run from inside the repo so `--repo` isn't needed, and use sensible defaults so `log` works with no options.
- Look at a simple UI or a GitHub integration, now that the core works. We'll test with the same kind of users again.

## Limits

Two testers is a small sample, and both used our demo repo, not their own. We wrote down what they said, not numbers, so we still need to measure accepted drafts and lookup time, ideally in a lab's own repo.
