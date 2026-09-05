# Personal Expense Tracker CLI

A lightweight, single-file Python CLI tool for logging and summarizing personal expenses. Data persists locally in a CSV file.

## Features

- **Add expenses** with date, amount, category, and optional notes
- **List expenses** with optional month filtering
- **View summaries** per category for any month, sorted by highest spending
- **Data persistence** using a local CSV file
- **Input validation** with clear error messages
- **Standard library only** — no external dependencies

## Requirements

- Python 3.6+

## Installation

1. Clone or download this repository
2. Ensure `tracker.py` is in your working directory
3. No installation or dependencies needed!

## Usage

### Add an Expense

```bash
python3 tracker.py add --amount <amount> --category <category> [--date YYYY-MM-DD] [--note "note"]
```

**Parameters:**
- `--amount`: Expense amount (required, must be > 0)
- `--category`: Expense category (required)
- `--date`: Date in YYYY-MM-DD format (optional, defaults to today)
- `--note`: Optional description of the expense

**Examples:**
```bash
python3 tracker.py add --amount 12.50 --category food --date 2026-07-01
python3 tracker.py add --amount 50 --category transport --note "Gas for car"
python3 tracker.py add --amount 100 --category utilities  # defaults to today
```

### List Expenses

```bash
python3 tracker.py list [--month YYYY-MM]
```

**Parameters:**
- `--month`: Filter by month in YYYY-MM format (optional)

**Examples:**
```bash
python3 tracker.py list                    # Show all expenses
python3 tracker.py list --month 2026-07   # Show only July 2026
```

### View Summary

```bash
python3 tracker.py summary --month YYYY-MM
```

**Parameters:**
- `--month`: Month to summarize in YYYY-MM format (required)

**Examples:**
```bash
python3 tracker.py summary --month 2026-07
```

Output shows:
- Total spending per category (sorted by highest to lowest)
- Grand total for the month

## Data Storage

Expenses are stored in `expenses.csv` in the working directory:

```csv
date,amount,category,note
2026-07-01,12.50,food,Lunch
2026-07-05,50.00,transport,Gas
2026-07-10,100.00,utilities,Monthly bill
```

The CSV file is created automatically on first use.

## Error Handling

The tool validates all inputs and provides clear error messages:

- **Invalid date**: Must be in YYYY-MM-DD format
- **Invalid amount**: Must be a number greater than 0
- **File errors**: Clear messages if CSV cannot be read/written

All errors exit with non-zero status and do not corrupt the CSV file.

## Testing

Run the comprehensive test suite:

```bash
python3 test_tracker.py
```

The test suite covers:
- ✓ Adding valid expenses
- ✓ Rejecting negative amounts
- ✓ Rejecting non-numeric amounts
- ✓ Filtering list by month
- ✓ Category summary with correct totals and sorting
- ✓ Handling empty data gracefully

## Implementation Notes

- **Single file**: Everything is in `tracker.py`
- **Standard library only**: Uses `argparse`, `csv`, `datetime`, and `pathlib`
- **CSV storage**: Human-readable format, easy to edit or export
- **No external dependencies**: Works anywhere Python 3.6+ is available

## License

This project is provided as-is for educational and personal use.
