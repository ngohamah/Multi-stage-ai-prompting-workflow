#!/usr/bin/env python3
"""Personal Expense Tracker CLI - log and summarize expenses from a CSV file."""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path


CSV_FILE = "expenses.csv"
CSV_HEADER = ["date", "amount", "category", "note"]


def init_csv():
    """Initialize CSV file with header if it doesn't exist."""
    if not Path(CSV_FILE).exists():
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)


def add_expense(amount, category, date=None, note=""):
    """Add an expense to the CSV file.
    
    Args:
        amount: float > 0
        category: string
        date: YYYY-MM-DD format (defaults to today)
        note: optional string
        
    Returns:
        True if successful, False if validation failed
    """
    init_csv()
    
    # Validate amount
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        print(f"Error: amount must be a number, got '{amount}'")
        return False
    
    if amount <= 0:
        print(f"Error: amount must be greater than 0, got {amount}")
        return False
    
    # Validate and format date
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: invalid date format '{date}', expected YYYY-MM-DD")
            return False
    
    # Append to CSV
    try:
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            # Format amount to 2 decimal places
            formatted_amount = f"{amount:.2f}"
            writer.writerow([date, formatted_amount, category, note])
        return True
    except Exception as e:
        print(f"Error: failed to write to {CSV_FILE}: {e}")
        return False


def list_expenses(month=None):
    """List all expenses, optionally filtered by month (YYYY-MM)."""
    init_csv()
    
    try:
        with open(CSV_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            expenses = list(reader)
    except Exception as e:
        print(f"Error: failed to read {CSV_FILE}: {e}")
        return False
    
    if not expenses:
        print("No expenses recorded.")
        return True
    
    # Filter by month if provided
    if month:
        expenses = [e for e in expenses if e["date"].startswith(month)]
    
    if not expenses:
        print(f"No expenses found for month {month}")
        return True
    
    # Print table header
    print(f"{'Date':<12} {'Amount':>10} {'Category':<15} {'Note':<20}")
    print("-" * 60)
    
    # Print rows
    for expense in expenses:
        date = expense["date"]
        amount = expense["amount"]
        category = expense["category"]
        note = expense["note"]
        print(f"{date:<12} {float(amount):>10.2f} {category:<15} {note:<20}")
    
    return True


def summary(month):
    """Print per-category totals for a given month, sorted descending by amount."""
    init_csv()
    
    if not month:
        print("Error: summary requires --month YYYY-MM")
        return False
    
    try:
        with open(CSV_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            expenses = list(reader)
    except Exception as e:
        print(f"Error: failed to read {CSV_FILE}: {e}")
        return False
    
    # Filter by month
    expenses = [e for e in expenses if e["date"].startswith(month)]
    
    if not expenses:
        print("No expenses found")
        return True
    
    # Aggregate by category
    by_category = {}
    for expense in expenses:
        category = expense["category"]
        amount = float(expense["amount"])
        by_category[category] = by_category.get(category, 0) + amount
    
    # Sort by amount descending
    sorted_categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
    
    # Print summary
    print(f"Expense Summary for {month}")
    print("-" * 40)
    
    grand_total = 0
    for category, total in sorted_categories:
        print(f"{category:<20} ${total:>10.2f}")
        grand_total += total
    
    print("-" * 40)
    print(f"{'TOTAL':<20} ${grand_total:>10.2f}")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Personal Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # add command
    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("--amount", required=True, help="Expense amount (must be > 0)")
    add_parser.add_argument("--category", required=True, help="Expense category")
    add_parser.add_argument("--date", default=None, help="Date in YYYY-MM-DD format (default: today)")
    add_parser.add_argument("--note", default="", help="Optional note")
    
    # list command
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.add_argument("--month", default=None, help="Filter by month (YYYY-MM)")
    
    # summary command
    summary_parser = subparsers.add_parser("summary", help="Summary by category for a month")
    summary_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    
    args = parser.parse_args()
    
    if args.command == "add":
        success = add_expense(
            amount=args.amount,
            category=args.category,
            date=args.date,
            note=args.note
        )
        sys.exit(0 if success else 1)
    
    elif args.command == "list":
        success = list_expenses(month=args.month)
        sys.exit(0 if success else 1)
    
    elif args.command == "summary":
        success = summary(month=args.month)
        sys.exit(0 if success else 1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
