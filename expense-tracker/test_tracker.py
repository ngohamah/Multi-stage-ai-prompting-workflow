#!/usr/bin/env python3
"""Test suite for Personal Expense Tracker CLI."""

import csv
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


class TestRunner:
    def __init__(self):
        self.test_dir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.test_dir, "expenses.csv")
        self.passed = 0
        self.failed = 0
        self.tracker_script = "tracker.py"
        # Copy tracker.py to the temp directory
        shutil.copy("tracker.py", self.test_dir)
        
    def run_command(self, *args):
        """Run tracker.py with given arguments and return (exit_code, stdout, stderr)."""
        cmd = ["python3", self.tracker_script] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.test_dir)
        return result.returncode, result.stdout, result.stderr
    
    def setup_test(self):
        """Create a fresh CSV for each test."""
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
    
    def get_csv_content(self):
        """Read and return CSV file content."""
        if not os.path.exists(self.csv_file):
            return []
        with open(self.csv_file, "r", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def assert_true(self, condition, message):
        """Assert that condition is True."""
        if condition:
            self.passed += 1
            print(f"  ✓ {message}")
        else:
            self.failed += 1
            print(f"  ✗ {message}")
    
    def assert_equal(self, actual, expected, message):
        """Assert that actual equals expected."""
        if actual == expected:
            self.passed += 1
            print(f"  ✓ {message}")
        else:
            self.failed += 1
            print(f"  ✗ {message} (expected {expected}, got {actual})")
    
    def test_case_1_add_valid_expense(self):
        """TC1: add --amount 12.50 --category food --date 2026-07-01"""
        print("\n[TC1] Add valid expense with specific date")
        print("  Command: python3 tracker.py add --amount 12.50 --category food --date 2026-07-01")
        self.setup_test()
        
        exit_code, stdout, stderr = self.run_command(
            "add", "--amount", "12.50", "--category", "food", "--date", "2026-07-01"
        )
        
        self.assert_equal(exit_code, 0, "Exit code is 0")
        
        csv_content = self.get_csv_content()
        self.assert_equal(len(csv_content), 1, "One row added to CSV")
        
        if csv_content:
            row = csv_content[0]
            self.assert_equal(row["date"], "2026-07-01", "Date is correct")
            self.assert_equal(row["amount"], "12.50", "Amount is correct")
            self.assert_equal(row["category"], "food", "Category is correct")
    
    def test_case_2_add_negative_amount(self):
        """TC2: add --amount -5 --category food"""
        print("\n[TC2] Add expense with negative amount (should error)")
        print("  Command: python3 tracker.py add --amount -5 --category food")
        self.setup_test()
        
        exit_code, stdout, stderr = self.run_command(
            "add", "--amount", "-5", "--category", "food"
        )
        
        self.assert_equal(exit_code, 1, "Exit code is 1 (error)")
        
        csv_content = self.get_csv_content()
        self.assert_equal(len(csv_content), 0, "No row added to CSV")
        
        self.assert_true("Error" in stdout or "Error" in stderr, "Error message printed")
    
    def test_case_3_add_non_numeric_amount(self):
        """TC3: add --amount abc --category food"""
        print("\n[TC3] Add expense with non-numeric amount (should error)")
        print("  Command: python3 tracker.py add --amount abc --category food")
        self.setup_test()
        
        exit_code, stdout, stderr = self.run_command(
            "add", "--amount", "abc", "--category", "food"
        )
        
        self.assert_equal(exit_code, 1, "Exit code is 1 (error)")
        
        csv_content = self.get_csv_content()
        self.assert_equal(len(csv_content), 0, "No row added to CSV")
        
        self.assert_true("Error" in stdout or "Error" in stderr, "Error message printed")
    
    def test_case_4_list_by_month(self):
        """TC4: list --month 2026-07"""
        print("\n[TC4] List expenses filtered by month")
        print("  Command: python3 tracker.py list --month 2026-07")
        self.setup_test()
        
        # Add multiple expenses in different months
        self.run_command("add", "--amount", "10", "--category", "food", "--date", "2026-07-01")
        self.run_command("add", "--amount", "20", "--category", "transport", "--date", "2026-07-15")
        self.run_command("add", "--amount", "30", "--category", "food", "--date", "2026-08-01")
        
        exit_code, stdout, stderr = self.run_command("list", "--month", "2026-07")
        
        self.assert_equal(exit_code, 0, "Exit code is 0")
        
        self.assert_true("2026-07-01" in stdout, "July 1st entry shown")
        self.assert_true("2026-07-15" in stdout, "July 15th entry shown")
        self.assert_true("2026-08-01" not in stdout, "August entry not shown")
        self.assert_true("10.00" in stdout, "Amount 10.00 shown")
        self.assert_true("20.00" in stdout, "Amount 20.00 shown")
    
    def test_case_5_summary_by_category(self):
        """TC5: summary --month 2026-07"""
        print("\n[TC5] Summary by category, descending by amount")
        print("  Command: python3 tracker.py summary --month 2026-07")
        self.setup_test()
        
        # Add multiple expenses in July
        self.run_command("add", "--amount", "10", "--category", "food", "--date", "2026-07-01")
        self.run_command("add", "--amount", "5", "--category", "food", "--date", "2026-07-05")
        self.run_command("add", "--amount", "30", "--category", "transport", "--date", "2026-07-10")
        self.run_command("add", "--amount", "20", "--category", "utilities", "--date", "2026-07-15")
        
        exit_code, stdout, stderr = self.run_command("summary", "--month", "2026-07")
        
        self.assert_equal(exit_code, 0, "Exit code is 0")
        
        self.assert_true("transport" in stdout, "Transport category shown")
        self.assert_true("utilities" in stdout, "Utilities category shown")
        self.assert_true("food" in stdout, "Food category shown")
        self.assert_true("30.00" in stdout, "Transport total 30.00 shown")
        self.assert_true("20.00" in stdout, "Utilities total 20.00 shown")
        self.assert_true("15.00" in stdout, "Food total 15.00 shown")
        self.assert_true("65.00" in stdout, "Grand total 65.00 shown")
        
        # Verify descending order: transport (30) should come before utilities (20), then food (15)
        transport_idx = stdout.find("transport")
        utilities_idx = stdout.find("utilities")
        food_idx = stdout.find("food")
        
        self.assert_true(
            transport_idx < utilities_idx < food_idx,
            "Categories sorted descending by amount"
        )
    
    def test_case_6_summary_no_data(self):
        """TC6: summary --month 2099-01"""
        print("\n[TC6] Summary for month with no data")
        print("  Command: python3 tracker.py summary --month 2099-01")
        self.setup_test()
        
        exit_code, stdout, stderr = self.run_command("summary", "--month", "2099-01")
        
        self.assert_equal(exit_code, 0, "Exit code is 0")
        self.assert_true("No expenses found" in stdout, "'No expenses found' message shown")
        self.assert_true("Error" not in stdout and "Error" not in stderr, "No error message")
    
    def run_all_tests(self):
        """Run all test cases."""
        print("=" * 60)
        print("Running Expense Tracker Test Suite")
        print("=" * 60)
        
        self.test_case_1_add_valid_expense()
        self.test_case_2_add_negative_amount()
        self.test_case_3_add_non_numeric_amount()
        self.test_case_4_list_by_month()
        self.test_case_5_summary_by_category()
        self.test_case_6_summary_no_data()
        
        print("\n" + "=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)
        
        return self.failed == 0


if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)
