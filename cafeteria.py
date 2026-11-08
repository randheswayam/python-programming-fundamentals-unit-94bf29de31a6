"""Cafeteria menu and daily specials.

Prints the fixed menu with a loop, then asks for a 
day of the week and uses
conditionals to decide which item is the special. 
"""
#The fixed menu each enters is in brackets: item name, price in dollars. 
MENU = [
    ("Tomato soup", 3.50),
    ("Grilled cheese sandwich", 4.25),
    ("Veggie wrap", 5.00),
    ("Chicken curry", 6.75),
    ("Fish and chips", 7.50),
    ("Garden salad", 4.00),
    ("Apple pie", 2.25),
]
def menu_lines():
    """Build one text line per menu item. Example: tomato soup $3.50 """
    lines = []
    for name, price in MENU:
        lines.append(f"{name:<25}${price:.2f}")
    return lines

def print_menu():
    """Print the menu."""
    print("===== Today's Menu =====")
    for line in menu_lines():
        print(line)

def price_of(item_name):
    """Return the menu price of item_name, or 0.0 if it is not on the menu."""
    for name, price in MENU:
        if name.lower() == item_name.strip().lower():
            return price
    return 0.0

def find_special(day):
    """Return(item name, discount) for the special of the day, or (None, 0.0) if no special.
    The discount is a fraction, e.g. 0.15 for 15% off."""
    chosen = day.strip().lower()
    if chosen == "monday":
        return ("Tomato soup", 0.20)
    elif chosen == "tuesday":
        return ("Grilled cheese sandwich", 0.10)
    elif chosen == "wednesday":
        return ("Veggie wrap", 0.15)
    elif chosen == "thursday":
        return ("Chicken curry", 0.25)
    elif chosen == "friday":
        return ("Fish and chips", 0.30)
    else:
        return (None,0.0)

def discount_price(full_price, discount):
    """Return the price after applying the discount."""
    return round(full_price * (1.0 - discount), 2)

def main():
    """Print the menu, ask for a day of the week, and print the special."""
    print_menu()
    day = input("Enter a day of the week to see the special: ")
    item, discount = find_special(day)
    if item is None:
        print("No special today.")
    else:
        full_price = price_of(item)
        sale_price = discount_price(full_price, discount)
        print(f"Today's special: {item}")
        print(f"Was ${full_price:.2f},now ${sale_price:.2f} Discount value: {discount} Discount type: {type(discount)}")

if __name__ == "__main__":
    main()