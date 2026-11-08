"""Tests for the cafeteria menu program."""
import subprocess
import sys
import unittest
from pathlib import Path

import cafeteria

SCRIPT = Path(__file__).parent / "cafeteria.py"

# Expected special for each weekday: (item, discount, full price, sale price).
WEEKDAY_SPECIALS = {
    "Monday": ("Tomato soup", 0.20, 3.50, 2.80),
    "Tuesday": ("Grilled cheese sandwich", 0.10, 4.25, 3.83),
    "Wednesday": ("Veggie wrap", 0.15, 5.00, 4.25),
    "Thursday": ("Chicken curry", 0.25, 6.75, 5.06),
    "Friday": ("Fish and chips", 0.30, 7.50, 5.25),
}


def run_program(typed_day):
    """Run cafeteria.py as a student would, answering the prompt with typed_day."""
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=typed_day + "\n",
        capture_output=True,
        text=True,
        timeout=30,
    )


class MenuTests(unittest.TestCase):
    def test_menu_has_seven_items(self):
        self.assertEqual(len(cafeteria.MENU), 7)

    def test_every_item_and_price_is_printed(self):
        lines = cafeteria.menu_lines()
        self.assertEqual(len(lines), len(cafeteria.MENU))
        for name, price in cafeteria.MENU:
            matching = [line for line in lines if line.startswith(name)]
            self.assertEqual(len(matching), 1, f"{name} is missing from the menu")
            self.assertIn(f"${price:.2f}", matching[0])

    def test_price_of_known_item(self):
        self.assertEqual(cafeteria.price_of("Tomato soup"), 3.50)

    def test_price_of_is_case_insensitive(self):
        self.assertEqual(cafeteria.price_of("veggie WRAP"), 5.00)

    def test_price_of_unknown_item_is_zero(self):
        self.assertEqual(cafeteria.price_of("Birthday Cake"), 0.00)


class SpecialTests(unittest.TestCase):
    def test_find_special_for_each_day(self):
        for day, (expected_item, expected_discount, _, _) in WEEKDAY_SPECIALS.items():
            with self.subTest(day=day):
                item, discount = cafeteria.find_special(day)
                self.assertEqual(item, expected_item)
                self.assertEqual(discount, expected_discount)

    def test_every_special_is_on_the_menu(self):
        for day in WEEKDAY_SPECIALS:
            with self.subTest(day=day):
                item, _ = cafeteria.find_special(day)
                self.assertGreater(cafeteria.price_of(item), 0.0)

    def test_discount_price_for_each_day(self):
        for day, (_, _, full_price, sale_price) in WEEKDAY_SPECIALS.items():
            with self.subTest(day=day):
                item, discount = cafeteria.find_special(day)
                self.assertEqual(cafeteria.price_of(item), full_price)
                self.assertEqual(cafeteria.discount_price(full_price, discount), sale_price)

    def test_monday_discount_price(self):
        item, discount = cafeteria.find_special("Monday")
        price = cafeteria.price_of(item)
        self.assertEqual(cafeteria.discount_price(price, discount), 2.80)

    def test_zero_discount_keeps_full_price(self):
        self.assertEqual(cafeteria.discount_price(4.00, 0.0), 4.00)

    def test_day_is_case_insensitive_and_ignores_spaces(self):
        self.assertEqual(cafeteria.find_special("  monday "), ("Tomato soup", 0.20))
        self.assertEqual(cafeteria.find_special("FRIDAY"), ("Fish and chips", 0.30))

    def test_weekend_has_no_special(self):
        self.assertEqual(cafeteria.find_special("Saturday"), (None, 0.0))
        self.assertEqual(cafeteria.find_special("Sunday"), (None, 0.0))

    def test_nonsense_day_has_no_special(self):
        self.assertEqual(cafeteria.find_special("Blursday"), (None, 0.0))
        self.assertEqual(cafeteria.find_special(""), (None, 0.0))

    def test_discount_is_always_a_float(self):
        for day in list(WEEKDAY_SPECIALS) + ["Saturday", "Sunday", "Blursday"]:
            with self.subTest(day=day):
                _, discount = cafeteria.find_special(day)
                self.assertIsInstance(discount, float)
                self.assertEqual(str(type(discount)), "<class 'float'>")


class ProgramRunTests(unittest.TestCase):
    def test_monday_run_prints_menu_special_and_type(self):
        result = run_program("Monday")
        self.assertEqual(result.returncode, 0, result.stderr)
        out = result.stdout
        for name, price in cafeteria.MENU:
            self.assertIn(name, out)
            self.assertIn(f"${price:.2f}", out)
        self.assertIn("Today's special: Tomato soup", out)
        self.assertIn("Was $3.50,now $2.80", out)
        self.assertNotIn("No special today", out)

    def test_every_weekday_run_prints_its_special(self):
        for day, (item, _, full_price, sale_price) in WEEKDAY_SPECIALS.items():
            with self.subTest(day=day):
                result = run_program(day)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"Today's special: {item}", result.stdout)
                self.assertIn(f"Was ${full_price:.2f},now ${sale_price:.2f}", result.stdout)

    def test_invalid_day_run_says_no_special(self):
        result = run_program("funday")
        self.assertEqual(result.returncode, 0, result.stderr)
        out = result.stdout
        self.assertIn("No special today", out)
        self.assertNotIn("Today's special", out)

    def test_weekend_run_says_no_special(self):
        result = run_program("Sunday")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No special today", result.stdout)

    def test_program_exits_after_one_answer(self):
        result = run_program("Monday")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        # The last thing printed is the type line, then the program ends.
        last_line = result.stdout.strip().splitlines()[-1]
        self.assertIn("Discount type: <class 'float'>", last_line)


if __name__ == "__main__":
    unittest.main()
