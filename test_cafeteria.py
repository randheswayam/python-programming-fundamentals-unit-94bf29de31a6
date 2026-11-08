"""Test for the cafeteria menu program."""
import subprocess
import sys 
from pathlib import Path
import unittest 
import cafeteria
SCRIPT = Path(__file__).parent / "cafeteria.py"
def run_program(typed_day):
    """run cafeteria. py as the students would,
    answering the prompt with typed day."""
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=typed_day + "\n",
        capture_output=True,
        text=True,
        timeout=30
    )


class MenuTests(unittest.TestCase):
    def test_menu_has_seveb_items(self):
        self.assertEqual(len(cafeteria.MENU),7)


    def test_every_item_and_price_is_printed(self):
        lines = cafeteria.menu_lines()
        self.assertEqual(len(lines),len(cafeteria.MENU))
        for name, price in cafeteria.MENU:
            matching = [line for line in lines if line.startswith(name)]
            self.assertEqual(len(matching),1, f"{name} is missing from the menu")
            self.assertIn(f"${price:.2f}", matching[0])
    def test_price_of_known_item(self):
        self.assertEqual(cafeteria.price_of("Tomato soup"),3.50)
    def test_price_of_unknown_item_is_zero(self):
        self.assertEqual(cafeteria.price_of("Birthday Cake"),0.00)

class SpecialTests(unittest.TestCase):
    def test_find_special_for_each_day(self):
        item, discount = cafeteria.find_special("Monday")
        self.assertEqual(item, "Tomato soup")
        self.assertEqual(discount, 0.20)
    def test_monday_discount_price(self):
        item, discount = cafeteria.find_special("Monday")
        price = cafeteria.price_of(item)

    def test_day_is_case_insensitive_and_ignores_spaces(self):
        self.assertEqual(cafeteria.find_special("  monday "), ("Tomato soup", 0.20))

    def test_weekend_has_no_special(self):
        self.assertEqual(cafeteria.find_special("Saturday"), (None, 0.0))
        self.assertEqual(cafeteria.find_special("Sunday"), (None, 0.0))

    def test_nonsense_day_has_no_special(self):
        self.assertEqual(cafeteria.find_special("Blursday"), (None, 0.0))

    def test_discount_is_always_a_float(self):
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            _, discount = cafeteria.find_special(day)
            self.assertIsInstance(discount, float)
            self.assertEqual(str(type(discount)), "<class 'float'>")

class programRunTests(unittest.TestCase):
    def test_monday_run_print_menu_special_and_type(self):
        result = run_program("Monday")
        self.assertEqual(result.returncode, 0, result.stderr)
        out = result.stdout
        for name, price in cafeteria.MENU:
            self.assertIn(name, out)
            self.assertIn(f"${price:.2f}", out)
        self.assertIn("Today's special: Tomato soup", out)
        self.assertIn("Was $3.50,now $2.80", out)
        self.assertNotIn("No special today", out)

    def test_invalid_day_run_say_no_special(self):
        result = run_program("funday")
        self.assertEqual(result.returncode, 0, result.stderr)
        out = result.stdout
        self.assertIn("No special today", out)
        self.assertNotIn("Today's special", out)

    def test_program_exists_after_one_answer(self):
        result = run_program("Monday")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        # the last thing printed is the type line, then the program ends.add(element)
        last_line = result.stdout.strip().splitlines()[-1]
        self.assertIn("Discount type: <class 'float'>", last_line)

if __name__ == "__main__":
    unittest.main()

        