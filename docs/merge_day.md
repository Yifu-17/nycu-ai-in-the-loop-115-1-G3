# Merge Day: Group 03

Date: 2026-11-23
Present: 陳繹夫, 吳傢澂, 吳承霖, 楊敦傑

---

## Part 0 ★ | The steward's merge plan (before the session, ~15 min, the current code steward)

Write this as a new entry in `DECISIONS.md` **before** the session, so everyone can read it first.

**List every open branch and pull request:**

| # | Branch / PR | What it does (one line) | Author | Ready? (yes / needs work / close it) | Touches the same files as… |
|---|---|---|---|---|---|
| 1 | #18 jcwu/compare | compare two branches with logged reasons | 吳傢澂 | yes | none |
| 2 | #17 tcyang/history | setting history and end to end test | 楊敦傑 | yes, after compare is merged | none, but its end to end test runs compare |
| 3 | #19 clwu/prompt-tests | 12 prompt test cases and the runner | 吳承霖 | yes if it has API results | none |

**Merge order** (and why this order: for example "small and independent first", "the shared data model before the features that use it"):

> 1. #18 compare
> 2. #17 history
> 3. #19 prompt-tests
>
> history's end to end test runs compare, so compare has to be merged first. prompt-tests only adds test files, and it goes last because it needs the API key.

**Conflicts we expect** (which files, between which PRs):

> None. The three PRs don't touch the same files.

**What "done" means today** (one sentence: what must run end to end?):

> On a fresh clone of main, pytest passes and log, history and compare all give real output on the demo repo.

**PRs we will close without merging, and why:**

> None.

---

## Part 1 | Agree the plan (5 min)

Read the steward's plan together. Change the order if someone sees a problem. Then decide who **drives** (types) for each merge: rotate so at least three of you drive.

| Merge # | Driver | Reviewer on screen |
|---|---|---|
| 1 | 吳傢澂 | 吳承霖 |
| 2 | 楊敦傑 | 陳繹夫 |
| 3 | 吳承霖 | 楊敦傑 |
| 4 | | |

We kept the steward's order. #19 was not merged today because we still don't have the API key.

---

## Part 2 ★ | Merge one at a time (about 35 min)

For **each** pull request, in plan order:

1. **Update it with `main`** (`git pull origin main` on the branch, or "Update branch" on GitHub)
2. **Conflicts? Resolve them together.** Read both sides out loud. If an AI tool proposes a resolution, the driver explains what it keeps and what it drops **before** you accept it. If nobody can explain it, resolve that part by hand
3. **Run the tests and the app** on the branch
4. **Review and merge** (the reviewer on screen approves, with at least one real comment if they have one)
5. **Run the tests and the app again on `main`**. Only then go to the next one

| # | PR | Conflicts? (where) | How we resolved them | Tests after merge (pass / fail) | App runs on `main`? |
|---|---|---|---|---|---|
| 1 | #18 compare | No | | Fail at first on Windows. Bare `pytest` couldn't import whychanged, and `python -m pytest` gave 18 passed, 1 failed because `bash` ran WSL bash. 吳傢澂 added `pythonpath = .` to pytest.ini and used the bash that ships with git (6d38a5b). Then 19 passed | Yes |
| 2 | #17 history | No | | After Update branch, the end to end test failed on Windows with the same WSL bash problem. 楊敦傑 used the same fix in test_end_to_end.py. Then 23 passed | Yes, history and compare give real output |
| 3 | #19 prompt-tests | | | Not merged, waiting for the API key | |
| 4 | | | | | |

**If something breaks on `main`:** stop merging. Fix it now (one small PR), or revert the last merge (`git revert -m 1 <merge commit>`) and write down why. Do not stack more merges on a broken `main`.

---

## Part 3 ★ | The fresh-clone test (10 min)

Someone who is **not** the steward:

1. Clones the repository into a **new folder** (`git clone <repo> merge_day_check`)
2. Follows **only the README** to install and run it
3. Does the **main task** of your tool from start to finish

| | |
|---|---|
| Who did it | 吳承霖, on Windows |
| Did the README work without help? (yes / partly / no) | Yes |
| What was missing from the README? | It only had Mac and Linux commands. We added the Windows ones: use Git Bash, `source .venv/Scripts/activate`, and `python -m pytest` |
| Did the main task work end to end? | Yes, init, log, history and compare all ran |
| Any API key or setup step that only one person knows? | No. The tool runs offline without a key. The API key is only needed for the prompt tests in #19 |

Fix small README gaps now. Anything bigger becomes an issue.

---

## Part 4 ★ | Record the outcome (5 min)

**Add the outcome under the steward's merge plan in `DECISIONS.md`:**

> **Outcome (2026-11-23):** merged #18 and #17. #19 is left open until we get the API key. No conflicts. The tests failed on Windows at first, fixed in both PRs before merging. Fresh-clone test by 吳承霖 on Windows: worked. `main` is green, 23 passed. Left for later: #19, issues #15, #21.

**Team check** (honestly, in a line each):

1. What made merging harder than it needed to be? (for example: long-lived branches, big PRs, two people editing the same file)
   #17 only passed after #18 was merged, and the tests had only been run on Mac, so both PRs failed on Windows.
2. One habit we will change for Phase 3:
   Before opening a PR, run pytest on both Windows and Mac, or ask someone on the other system to run it.
3. Could each of us run the prototype and do the main task without help? If not, who will practise with whom before CP2?
   Yes. After the Windows fixes everyone ran it on their own laptop.
