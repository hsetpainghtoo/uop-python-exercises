def print_circum(radius):
    pi = 3.14159
    circumference = 2 * pi * radius
    print(f"The circumference of a circle with radius {radius} is {circumference}")


def display_magic_catalog():
    """
    Calculates and displays the catalog for Merlin's Magic Mart,
    including discounts for duo spells and the wizard's triad pack.
    """
    # 1. Assignment Statements: Defining prices for individual magical items
    # Prices are floats to represent currency
    price_potion = 50.0   # Item 1
    price_scroll = 120.0  # Item 2
    price_wand = 300.0    # Item 3

    # 2. Expressions: Calculating Combo Prices (10% discount = 90% of sum)
    # Combo 1: Potion + Scroll
    combo_1_price = (price_potion + price_scroll) * 0.90

    # Combo 2: Scroll + Wand
    combo_2_price = (price_scroll + price_wand) * 0.90

    # Combo 3: Potion + Wand
    combo_3_price = (price_potion + price_wand) * 0.90

    # 3. Order of Operations: Calculating Gift Pack (25% discount = 75% of sum)
    # The Triad Pack (All three items)
    triad_pack_price = (price_potion + price_scroll + price_wand) * 0.75

    # 4. Output: Printing the formatted catalog
    print("Merlin's Magic Mart")
    print("-" * 45) # String repetition for a divider
    print("Artifact(s) \t\t\t\t\t\t Gold Coins")

    # Printing Individual Items
    print("1. Healing Potion \t\t\t\t\t", price_potion)
    print("2. Fire Scroll \t\t\t\t\t\t", price_scroll)
    print("3. Elder Wand \t\t\t\t\t\t", price_wand)

    # Printing Combos with discount % included in the string
    print("Duo 1 (Potion + Scroll) [10% off] \t", combo_1_price)
    print("Duo 2 (Scroll + Wand)   [10% off] \t", combo_2_price)
    print("Duo 3 (Potion + Wand)   [10% off] \t", combo_3_price)
    print("Triad Pack (All 3)      [25% off] \t", triad_pack_price)

    print("-" * 45)
    print("For owls send to: Tower-9-Platform-3/4")

# Executing the function
display_magic_catalog()