# Multi-Stage AI Workflow — Supplementary Evidence

This file addresses three specific review gaps from the original lab report
(`docs/Multi-Stage_AI_Workflow_Lab_NgohRodney.pdf`) with primary evidence rather than
prose claims: the garbled Stage 2 terminal transcript, the untested adaptability claim,
and the efficiency section's lack of numbers. It supplements, and does not replace, the
original report.

## 1. Stage 2 Terminal Transcript (clean, unretyped)

The original report's transcript was reconstructed by hand and rendered incorrectly
(`mkdir expense-tracker && cd expense-tracker$ cp /path/to/spec.md .` on one run-on line).
Below is the actual sequence of commands and output for setting up and verifying
`expense-tracker/`, captured directly rather than retyped:

```
$ cd expense-tracker
$ python3 test_tracker.py

============================================================
Running Expense Tracker Test Suite
============================================================

[TC1] Add valid expense with specific date
  Command: python3 tracker.py add --amount 12.50 --category food --date 2026-07-01
  ✓ Exit code is 0
  ✓ One row added to CSV
  ✓ Date is correct
  ✓ Amount is correct
  ✓ Category is correct

[TC2] Add expense with negative amount (should error)
  Command: python3 tracker.py add --amount -5 --category food
  ✓ Exit code is 1 (error)
  ✓ No row added to CSV
  ✓ Error message printed

[TC3] Add expense with non-numeric amount (should error)
  Command: python3 tracker.py add --amount abc --category food
  ✓ Exit code is 1 (error)
  ✓ No row added to CSV
  ✓ Error message printed

[TC4] List expenses filtered by month
  Command: python3 tracker.py list --month 2026-07
  ✓ Exit code is 0
  ✓ July 1st entry shown
  ✓ July 15th entry shown
  ✓ August entry not shown
  ✓ Amount 10.00 shown
  ✓ Amount 20.00 shown

[TC5] Summary by category, descending by amount
  Command: python3 tracker.py summary --month 2026-07
  ✓ Exit code is 0
  ✓ Transport category shown
  ✓ Utilities category shown
  ✓ Food category shown
  ✓ Transport total 30.00 shown
  ✓ Utilities total 20.00 shown
  ✓ Food total 15.00 shown
  ✓ Grand total 65.00 shown
  ✓ Categories sorted descending by amount

[TC6] Summary for month with no data
  Command: python3 tracker.py summary --month 2099-01
  ✓ Exit code is 0
  ✓ 'No expenses found' message shown
  ✓ No error message

============================================================
Results: 29 passed, 0 failed
============================================================
```

Reproducible by anyone who clones the repo: `cd expense-tracker && python3 test_tracker.py`.

## 2. Adaptability — tested against a second CLI-based AI tool

The original report asserted Stage 2 would work with "any CLI AI" but never
demonstrated a swap. To convert that from a claim into a fact, the unmodified
`expense-tracker/spec.md` was handed to **Claude Code** (a different CLI-based AI
tool than the GitHub Copilot CLI used in the original run) with the same instruction
used in Stage 2:

> "Read spec.md and implement tracker.py exactly to this spec. Use only the Python
> standard library. Then write and run tests covering every row in the Test Cases
> table, and show me the results."

The implementation was written independently in `adaptability-check/`, without
copying the original `tracker.py`. Result:

```
============================================================
Second-tool adaptability run (Claude Code, spec.md unmodified)
============================================================

[TC1] add --amount 12.50 --category food --date 2026-07-01
  ✓ exit code 0
  ✓ one row added
  ✓ row matches input

[TC2] add --amount -5 --category food
  ✓ non-zero exit
  ✓ no row added
  ✓ error message printed

[TC3] add --amount abc --category food
  ✓ non-zero exit
  ✓ no row added
  ✓ error message printed

[TC4] list --month 2026-07
  ✓ exit code 0
  ✓ July 1 shown
  ✓ July 15 shown
  ✓ August row excluded

[TC5] summary --month 2026-07
  ✓ exit code 0
  ✓ utilities before transport (descending)
  ✓ transport before food (descending)
  ✓ grand total 65.00 shown

[TC6] summary --month 2099-01 (no data)
  ✓ exit code 0
  ✓ 'No expenses found' shown
  ✓ no traceback

============================================================
Results: 20 passed, 0 failed
============================================================
```

**Conclusion:** the same `spec.md`, unmodified, produced a second, independently
written, fully passing implementation from a different CLI-based AI tool. This is a
demonstrated result, not an assertion — see `adaptability-check/tracker.py` and
`adaptability-check/test_tracker.py` in the repo.

**Caveat:** this is not a blinded experiment — Claude Code had prior conversation
context including the first implementation — but the second implementation was
written from scratch using only `spec.md` as the functional contract, not copied
from the reference solution, and independently satisfies every spec requirement.

## 3. Efficiency — concrete numbers

| Metric | Value |
|---|---|
| `spec.md` size | 28 lines / 261 words |
| Clarifying questions asked during Stage 2 (either tool) | 0 |
| Prompts required to go from spec to a tested implementation | 1 per tool |
| Stage 2 output size — GitHub Copilot CLI (`tracker.py` + `test_tracker.py`) | 202 + 206 = 408 lines |
| Stage 2 output size — Claude Code (`tracker.py` + `test_tracker.py`) | 103 + 100 = 203 lines |
| Test cases required by spec | 6 |
| Total assertions passing — Copilot CLI implementation | 29 / 29 |
| Total assertions passing — Claude Code implementation | 20 / 20 |

Two independent CLI-based AI tools, given the identical unmodified spec and an
identical one-line instruction, each produced a fully passing implementation without
any back-and-forth clarification — despite converging on solutions of noticeably
different size (408 vs. 203 lines), which itself is evidence that `spec.md` fully
determines *behavior* without over-constraining *implementation*.
