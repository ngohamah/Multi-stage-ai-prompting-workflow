import csv
import subprocess
import sys
from pathlib import Path

WORKDIR = Path(__file__).parent
CSV_PATH = WORKDIR / "expenses.csv"

passed = 0
failed = 0


def check(label, condition):
    global passed, failed
    if condition:
        print(f"  ✓ {label}")
        passed += 1
    else:
        print(f"  ✗ {label}")
        failed += 1


def run(*args):
    return subprocess.run(
        [sys.executable, "tracker.py", *args],
        cwd=WORKDIR, capture_output=True, text=True,
    )


def reset():
    if CSV_PATH.exists():
        CSV_PATH.unlink()


def rows():
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open(newline="") as f:
        return list(csv.DictReader(f))


print("=" * 60)
print("Second-tool adaptability run (Claude Code, spec.md unmodified)")
print("=" * 60)

print("\n[TC1] add --amount 12.50 --category food --date 2026-07-01")
reset()
r = run("add", "--amount", "12.50", "--category", "food", "--date", "2026-07-01")
check("exit code 0", r.returncode == 0)
data = rows()
check("one row added", len(data) == 1)
check("row matches input", data and data[0] == {"date": "2026-07-01", "amount": "12.50", "category": "food", "note": ""})

print("\n[TC2] add --amount -5 --category food")
before = len(rows())
r = run("add", "--amount", "-5", "--category", "food")
check("non-zero exit", r.returncode != 0)
check("no row added", len(rows()) == before)
check("error message printed", "error" in (r.stdout + r.stderr).lower())

print("\n[TC3] add --amount abc --category food")
before = len(rows())
r = run("add", "--amount", "abc", "--category", "food")
check("non-zero exit", r.returncode != 0)
check("no row added", len(rows()) == before)
check("error message printed", "error" in (r.stdout + r.stderr).lower())

print("\n[TC4] list --month 2026-07")
reset()
run("add", "--amount", "10", "--category", "transport", "--date", "2026-07-01")
run("add", "--amount", "20", "--category", "transport", "--date", "2026-07-15")
run("add", "--amount", "99", "--category", "food", "--date", "2026-08-01")
r = run("list", "--month", "2026-07")
check("exit code 0", r.returncode == 0)
check("July 1 shown", "2026-07-01" in r.stdout)
check("July 15 shown", "2026-07-15" in r.stdout)
check("August row excluded", "2026-08-01" not in r.stdout)

print("\n[TC5] summary --month 2026-07")
reset()
run("add", "--amount", "10", "--category", "food", "--date", "2026-07-01")
run("add", "--amount", "5", "--category", "food", "--date", "2026-07-02")
run("add", "--amount", "20", "--category", "transport", "--date", "2026-07-03")
run("add", "--amount", "30", "--category", "utilities", "--date", "2026-07-04")
r = run("summary", "--month", "2026-07")
check("exit code 0", r.returncode == 0)
check("utilities before transport (descending)", r.stdout.index("utilities") < r.stdout.index("transport"))
check("transport before food (descending)", r.stdout.index("transport") < r.stdout.index("food"))
check("grand total 65.00 shown", "65.00" in r.stdout)

print("\n[TC6] summary --month 2099-01 (no data)")
r = run("summary", "--month", "2099-01")
check("exit code 0", r.returncode == 0)
check("'No expenses found' shown", "No expenses found" in r.stdout)
check("no traceback", "Traceback" not in r.stderr)

print("\n" + "=" * 60)
print(f"Results: {passed} passed, {failed} failed")
print("=" * 60)
sys.exit(1 if failed else 0)
