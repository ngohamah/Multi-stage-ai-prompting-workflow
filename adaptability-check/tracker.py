#!/usr/bin/env python3
import argparse
import csv
import sys
from datetime import date, datetime
from pathlib import Path

CSV_PATH = Path("expenses.csv")
HEADER = ["date", "amount", "category", "note"]


def ensure_csv():
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="") as f:
            csv.writer(f).writerow(HEADER)


def cmd_add(args):
    try:
        amount = float(args.amount)
    except ValueError:
        print(f"error: amount must be a number, got {args.amount!r}")
        return 1
    if amount <= 0:
        print(f"error: amount must be > 0, got {amount}")
        return 1

    if args.date is None:
        expense_date = date.today().isoformat()
    else:
        try:
            expense_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print(f"error: invalid date {args.date!r}, expected YYYY-MM-DD")
            return 1

    ensure_csv()
    with CSV_PATH.open("a", newline="") as f:
        csv.writer(f).writerow([expense_date, f"{amount:.2f}", args.category, args.note or ""])
    return 0


def read_rows():
    ensure_csv()
    with CSV_PATH.open(newline="") as f:
        return list(csv.DictReader(f))


def cmd_list(args):
    rows = read_rows()
    if args.month:
        rows = [r for r in rows if r["date"].startswith(args.month)]
    if not rows:
        print("No expenses found")
        return 0
    print(f"{'date':<12}{'amount':>10}  {'category':<12}note")
    for r in rows:
        print(f"{r['date']:<12}{float(r['amount']):>10.2f}  {r['category']:<12}{r['note']}")
    return 0


def cmd_summary(args):
    rows = [r for r in read_rows() if r["date"].startswith(args.month)]
    if not rows:
        print("No expenses found")
        return 0

    totals = {}
    for r in rows:
        totals[r["category"]] = totals.get(r["category"], 0.0) + float(r["amount"])

    grand_total = sum(totals.values())
    for category, total in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{category:<15}{total:>10.2f}")
    print(f"{'TOTAL':<15}{grand_total:>10.2f}")
    return 0


def main():
    parser = argparse.ArgumentParser(prog="tracker.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("--amount", required=True)
    p_add.add_argument("--category", required=True)
    p_add.add_argument("--date", default=None)
    p_add.add_argument("--note", default=None)
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list")
    p_list.add_argument("--month", default=None)
    p_list.set_defaults(func=cmd_list)

    p_summary = sub.add_parser("summary")
    p_summary.add_argument("--month", required=True)
    p_summary.set_defaults(func=cmd_summary)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
