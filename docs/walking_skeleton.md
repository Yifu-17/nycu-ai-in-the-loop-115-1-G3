# Walking Skeleton: Group 03

Date: 2026-11-21, 15:00
Present: 陳繹夫, 吳傢澂, 吳承霖, 楊敦傑
Shared screen: we took turns, each author shared their screen when their PR was reviewed

---

## Part 1 | What the tool does in one sentence

| | Sentence |
|---|---|
| 陳繹夫 | Our tool helps a research team on one repo see why each setting changed and who decided it, by having AI draft the reason and the author confirm it. |
| 吳傢澂 | Our tool helps research teams sharing a repo to trace why experiment settings changed by having authors confirm AI-drafted reasons for each change. |
| 吳承霖 | Our tool helps research teams find out why a shared experiment setting changed by having AI draft the reason from commit messages for the author to confirm. |
| 楊敦傑 | Our tool helps members of research teams who share one GitHub repo find out why a training config or environment variable changed and who decided it, by detecting changed settings in the git diff, having AI draft the reason from commit and PR context for the author to confirm, and saving it to a searchable log. |
| Agreed sentence | Our tool helps research teams sharing one GitHub repo find out why an experiment setting changed and who decided it, by having AI draft the reason from commit messages for the author to confirm. |

Did all four sentences match? ☐ Yes ☑ Mostly ☐ No

Difference we had to settle:

> Two of us didn't mention who decided the change. We put it back in the agreed sentence, since that's the part git log can't tell you. 楊敦傑's sentence also said the AI reads PR context and the log is searchable. The tool doesn't do either yet, so we left them out.

---

## Part 2 | The path and the split

The path:

```
[git diff of the watched settings files]
   -> [diff_parser: which settings changed]
   -> [drafter: one-line reason from commit messages, or "unknown"]
   -> [confirm: author accepts or edits it and types who decided]
   -> [store: saved to .whychanged/log.jsonl]
```

context.py reads the commit messages, branch and author and passes them to the drafter. It was already done in #10.

Where we are: ☑ Yes, Route 2. The skeleton from #10 already ran from start to end, just with fake modules.

Trace:

| Box | Explained by |
|---|---|
| cli.py and models.py | 吳承霖 |
| context.py | 楊敦傑 |
| stub modules | 吳傢澂 |

Boxes only their author could explain:

> None.

Our goal for today:

> Replace the three fake modules on the main path with real code. Input is the feat/head-dropout branch in our demo repo. Output is two log entries: dropout with the reason from the commit message, and batch_size as "unknown" until the author fills it in.

The split. We agreed on the data shapes in whychanged/models.py first, so everyone knew what to take in and give back.

| Person | Building task | Receives | Returns | Branch |
|---|---|---|---|---|
| 吳傢澂 | diff_parser | base, head, list of watched files | list of SettingChange | jcwu/diff-parser |
| 吳承霖 | drafter and CLAUDE.md | SettingChange, ChangeContext | Draft with reason, evidence, source | clwu/ai-drafter |
| 楊敦傑 | confirm and store | SettingChange, ChangeContext, Draft | LogEntry, added to log.jsonl | tcyang/confirm-store |
| 陳繹夫 | skeleton in #10, ran the demo after each merge | | | yifu/skeleton |

Things we left out on purpose today:

> history and compare are still fake, we'll do them next. No GitHub Action. We don't have an API key yet, so the drafter runs in offline mode.

---

## Part 3 | Build and connect

We didn't use one skeleton branch. Each person opened their own PR to main and we merged them in path order, so every piece got its own review. After each merge we ran the demo again.

| Piece | Built by | Explained by | Connected? | What we had to fix at the connection |
|---|---|---|---|---|
| diff_parser | 吳傢澂 | 吳承霖 | yes | nothing |
| drafter | 吳承霖 | 楊敦傑 | with a fix | CLAUDE.md didn't get committed in #12. The drafter needs it as the system prompt, otherwise a real API call fails and it just goes back to offline without telling anyone. 吳承霖 added it in #14. |
| confirm and store | 楊敦傑 | 陳繹夫 | yes | nothing |

Where it first ran end to end:

> Right after #13 was merged. We ran log on feat/head-dropout and got two entries: dropout with the reason taken from the commit message, and batch_size with a reason the author typed in.

What we faked or stubbed:

> The drafter uses the offline version because we have no API key. history and compare are still fake.

---

## Part 4 | Pull requests

| | PR 2 diff_parser | PR 3 drafter | PR 4 confirm and store |
|---|---|---|---|
| Link | [#11](https://github.com/Yifu-17/nycu-ai-in-the-loop-115-1-G3/pull/11) | [#12](https://github.com/Yifu-17/nycu-ai-in-the-loop-115-1-G3/pull/12), fixed in [#14](https://github.com/Yifu-17/nycu-ai-in-the-loop-115-1-G3/pull/14) | [#13](https://github.com/Yifu-17/nycu-ai-in-the-loop-115-1-G3/pull/13) |
| Reviewed by | 吳承霖 | 楊敦傑 | 陳繹夫 |
| Reviewer's comment | PyYAML reads 1e-3 as a string but 0.001 as a number, so if someone rewrites lr from 0.001 to 1e-3 it counts as a change. Should it? | If the API fails, does it fall back to offline? Then the author can't tell if the draft came from AI. Can the screen show where the draft came from? | If two people add to log.jsonl on different branches, it will conflict when we merge. How do we handle that? |
| Author's answer | Yes, right now it counts. But it's the same value written differently, so at worst we get one extra entry and never miss a real change. | Draft already has a source field that says ai or offline, it's just not shown. The change is in the confirm screen, so I'll add it after PR 4 is merged. Opened [#15](https://github.com/Yifu-17/nycu-ai-in-the-loop-115-1-G3/issues/15). | It will conflict, but each line is its own entry, so for now we just keep both sides. We'll deal with it when it happens. |

Line added to DECISIONS.md:

> Walking skeleton: kept the stubs from #10 so the whole path ran before any real code, then swapped in diff_parser, drafter and confirm/store one PR at a time. history and compare stay stubs until the next slice.

---

## Part 5 | Team check

1. What worked well in how we worked together today?

   > Since the skeleton and models.py were already in #10, everyone knew what their part had to take in and give back, so we could all work at the same time. Each part came with its own tests. #10 to #14 were all merged today.

2. What was hard or awkward?

   > The PRs had to be merged one by one, so everyone had to wait for the person before them. CLAUDE.md was missing from #12 and we didn't notice until we checked main after #13.

3. Who had the least chance to contribute, and what would help next time?

   > 陳繹夫 wrote the skeleton before the meeting, so the rest of us only saw cli.py and models.py during review. The trace helped but was pretty short. Next time each author should walk through their part for a couple of minutes before someone else explains it back.

4. One thing we will do differently on merge day:

   > Before merging, someone who isn't the author runs the whole demo once and checks that every file is really in the PR.

5. Blockers and who follows up:

   > No API key yet, so the drafter can only run offline. 陳繹夫 will ask the TA by 11/24.
