# Spec: Personal Expense Tracker CLI

## Purpose
A single-file Python CLI tool that lets a user log expenses and view a categorized monthly summary, reading/writing to a local CSV file.

## Functional Requirements
1. `add` — record an expense with: date (YYYY-MM-DD, default today), amount (float, > 0), category (string), note (optional string).
2. `list` — print all recorded expenses as a table, optionally filtered by `--month YYYY-MM`.
3. `summary` — print total spend per category for a given month, sorted descending by amount, plus a grand total.
4. Data persists in `expenses.csv` in the working directory with header: `date,amount,category,note`.
5. Invalid input (bad date, non-numeric amount, amount <= 0) must print a clear error and exit non-zero, without corrupting the CSV.

## Non-Functional Requirements
- Single file, standard library only (argparse, csv, datetime) — no external dependencies.
- Must run with `python3 tracker.py <command> [args]`.

## Test Cases
| # | Command | Expected Result |
|---|---------|------------------|
| 1 | `add --amount 12.50 --category food --date 2026-07-01` | Row appended to expenses.csv |
| 2 | `add --amount -5 --category food` | Error, non-zero exit, no row added |
| 3 | `add --amount abc --category food` | Error, non-zero exit, no row added |
| 4 | `list --month 2026-07` | Only July 2026 rows printed |
| 5 | `summary --month 2026-07` | Per-category totals + grand total, descending order |
| 6 | `summary --month 2099-01` (no data) | Prints "No expenses found" rather than crashing |

## Out of Scope
- Multi-currency support, budgets/alerts, GUI.
