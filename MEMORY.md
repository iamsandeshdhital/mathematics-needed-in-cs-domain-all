# MEMORY.md — Progress notes for this repository

## What this project is

A GitHub repo containing every piece of mathematics needed for computer science,
taught step by step. Public repo:

**https://github.com/iamsandeshdhital/mathematics-needed-in-cs-domain-all**

Local path: `C:\Users\NEPAL\OneDrive\Desktop\mathematics-needed-in-cs-domain-all`

GitHub token is stored at `C:\Users\NEPAL\OneDrive\Desktop\git token.txt`
(owner: `iamsandeshdhital`). Verified working. The `gh` CLI is **not** installed,
so the GitHub API is called with `urllib` in Python.

## Current status: COMPLETE AND PUSHED

| Item | Value |
| --- | --- |
| Lessons | 62 across 11 parts (`part00_…` … `part10_…`) |
| Part READMEs | 11 of 11 |
| Sections per lesson | 12 required sections, none missing, no duplicates |
| MCQs | 656, each with 4 options + per-distractor reasoning |
| Subjective | 363 short answer + 255 long answer, all with model answers |
| Code blocks | ~754 execute successfully (`python run_all.py`, exit 0) |
| Fence balance | 1126 blocks across 76 files, all balanced |
| Encoding damage | 0 occurrences of U+FFFD |
| Local vs remote | in sync, working tree clean |

Last commit pushed: `72a738a`.

## Lesson template (the contract every lesson follows)

Defined in `CONTRIBUTING.md`. Required `##` sections, in order:

```
In Plain Words / Why Computer Science Cares / The Formal Version /
Worked Example / Runnable Code / Common Mistakes /
Multiple Choice Questions / Subjective Questions /
Exercises and Solutions / Summary / Next
```

`## Formula Sheet` sits between The Formal Version and Worked Example in most
lessons. MCQ format: `**Q1.**` + options `- A)` … `- D)` + `<details>` with the
answer letter, full option text, then why each wrong option is wrong.
Subjective format: `### Short Answer` (4–6) and `### Long Answer` (3–5), each
`<details>` with a complete model answer.

## Verification tooling

- `python index.py` — prints the lesson index, grouped by part
- `python run_all.py` — extracts and executes every ```python block; must exit 0
- `python run_all.py part06_algorithms_math` — scope to one part (fast, ~2 min)
- **Always set `$env:OPENBLAS_NUM_THREADS=1`** before running, or OpenBLAS
  crashes with a memory error.
- Console cannot print non-ASCII: set `$env:PYTHONIOENCODING='utf-8'` first.

Fence checker (CommonMark-accurate, written to temp):
`C:\Users\NEPAL\AppData\Local\Temp\opencode\mdfence.py <file>`
Important: a bare ``` correctly CLOSES a block opened by ```. Naive counters
treat every ``` as an opener and report false "unbalanced" results.
`CONTRIBUTING.md` legitimately uses a 4-backtick fence, so it always reports a
false positive.

## Things already fixed — do not regress

- Broken `../../SYMBOLS.md` links (should be `../SYMBOLS.md`) across parts
- Lesson 25: prose said "5 classes / 4" where the code gives 4 / 3
- Lesson 10: Summary bullet said `¬P ∧ Q` where it meant `P ∧ Q`
- Lesson 10: Formula Sheet reduced to the standard 4 columns
- Lesson 81: **inverse-Ackermann definition was wrong** — now `A(0)=1`,
  `A(k+1)=2^{A(k)}` (a tower of **twos**, not threes). Correctly:
  `α(n) = min{k : A(k) >= n}`, giving `α(17)=3`, `A(3,3)=61`, `A(4,4)` is
  computationally intractable. `α(n) ≤ 4` for n ≤ 65536, `≤ 5` for all n.
- Lesson 81: accounting method corrected to `c_i = 3 - T_i`, `Φ = 2n - C`,
  identity `B_k = Φ_k - Φ_0`

## Known issues (do NOT trust agent reports on these)

- **Concurrent agents overwrite each other.** Several agents ran on this repo at
  once and clobbered each other's files mid-write, producing duplicated
  sections. Always verify with `git status`, `git diff --stat`, and by reading
  the file — never trust a completion report.
- **Agents have run `git commit` and `git push` without being asked.** Check
  `git log` before assuming a commit is yours.
- **Agents reported bugs that were false positives.** The "unclosed code fence"
  in lesson 81 was a miscounted bare ``` close.
- The `α(N) ≤ 4 for all 64-bit N` claim in the original lesson is right in
  spirit but the agent's earlier version had the wrong `A` definition.

## If continuing work

1. `git fetch origin && git status` — check nothing is half-written
2. Re-run `python run_all.py` scoped to the part you touched (set OPENBLAS=1)
3. Re-run the fence checker on the files you changed
4. Commit and push; verify `git rev-list --left-right --count origin/main...HEAD`
   returns `0  0`