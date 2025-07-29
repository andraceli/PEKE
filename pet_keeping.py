import json
import os
import random

# --- Game Constants ---
DATA_DIR = "venv"
DATA_FILE = os.path.join(DATA_DIR, "pet_game_data.json")

ANIMALS = {
    "1": "Elephant",
    "2": "Tiger",
    "3": "Lion",
    "4": "Python",
    "5": "Bear"
}

MAPS = {
    "1": "Zoo",
    "2": "Jungle",
    "3": "Cave"
}

MAP_DESCRIPTIONS = {
    "Zoo": "An abandoned zoo, where you might find leftover coins or rare chocolates.",
    "Jungle": "A lush jungle full of trees and plants. Mine for woods and leaves.",
    "Cave": "A dark cave, maybe you'll find shells or even golds hidden in the shadows."
}

MAP_ITEMS = {
    "Zoo": ["Unwanted Coins", "Chocolate"],
    "Jungle": ["Woods", "Leaves"],
    "Cave": ["Shells", "Golds"]
}

ITEM_VALUES = {
    "Unwanted Coins": [1, 3, 5, 10],  # random amount
    "Chocolate": 1, # just gets stored for loaders
    "Woods": 5,
    "Leaves": 10,
    "Shells": 1,
    "Golds": 1
}

ITEM_SELL_VALUES = {
    "Woods": (5, 10),    # 5 woods = 10 coins
    "Leaves": (10, 5),   # 10 leaves = 5 coins
    "Shells": (1, 3),    # 1 shell = 3 coins
    "Golds": (1, 5),     # 1 gold = 5 coins
}

SHOP_ITEMS = {
    "1": {"name": "Fresh fruits", "price": 5, "for": ["Elephant", "Bear"]},
    "2": {"name": "Raw meats", "price": 5, "for": ["Tiger", "Lion"]},
    "3": {"name": "Whole prey", "price": 5, "for": ["Python"]},
    "4": {"name": "Loaders (Chocolate)", "price": 10, "for": ["Elephant", "Tiger", "Lion", "Python", "Bear"]}
}

DEFAULT_DATA = {
    "animal_type": None,
    "animal_name": None,
    "lvl": 1,
    "xp": 0,
    "xp_limit": 10,
    "energy": 10,
    "energy_limit": 10,
    "coins": 100,
    "items": {},
    "foods": [],
    "chocolates_used": 0,
}

# --- Utility Functions ---
def ensure_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def prompt_int(msg, allowed):
    choice = input(msg)
    while choice not in allowed:
        print("Invalid option.")
        choice = input(msg)
    return choice

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- XP/Leveling Functions ---
def add_xp(data, amount=5):
    data["xp"] += amount
    leveled_up = False
    while data["xp"] >= data["xp_limit"]:
        data["xp"] -= data["xp_limit"]
        data["lvl"] += 1
        # New XP limit: random divisible by 5, 10-100
        xp_limit = random.choice([x for x in range(10, 101, 5)])
        data["xp_limit"] = xp_limit
        # New energy limit: random divisible by 10, 10-100
        energy_limit = random.choice([x for x in range(10, 101, 10)])
        data["energy_limit"] = energy_limit
        # When leveling up, refill energy to new limit
        data["energy"] = energy_limit
        leveled_up = True
        print(f"\nCongratulations! {data['animal_name']} leveled up to {data['lvl']}!")
        print(f"XP needed for next level: {data['xp_limit']}")
        print(f"New energy limit: {data['energy_limit']}")
    return leveled_up

# --- Game Introduction ---
def show_introduction():
    clear_screen()
    print("="*40)
    print("Welcome to: Pet Keeping")
    print("="*40)
    print("\nDescription:\nKeeping a pet being abandoned by the circus as dysfunctional animal for entertainment, the only thing they end up with is jungle, the worst is death.\n")
    input("\nPress Enter to continue...")
    clear_screen()
    print("\nWhen the only hope of your life is the house of entertainment, what if one day everything will be gone, what will happen if I die?\n")
    input("\nPress Enter to continue...")
    clear_screen()
    print("\nThe only thing I see is I am surrounded by excellent animals, in the end you don't know what's going on, is it bad or good?\n")
    input("\nPress Enter to continue...")

def choose_animal():
    clear_screen()
    print("--- Choose your animal ---")
    for k, v in ANIMALS.items():
        print(f"{k}. {v}")
    choice = prompt_int("Enter animal number: ", ANIMALS.keys())
    animal_type = ANIMALS[choice]
    animal_name = input(f"What would you like to name your {animal_type}? ").strip()
    while not animal_name:
        animal_name = input("Please enter a valid name: ").strip()
    print(f"You chose: {animal_type} named {animal_name}")
    input("Press Enter to continue...")
    return animal_type, animal_name

# --- Main Menu ---
def main_menu(data):
    while True:
        clear_screen()
        print("=== MAIN MENU ===")
        print(f"Name: {data['animal_name']} | Animal: {data['animal_type']} | Level: {data['lvl']} | XP: {data['xp']}/{data['xp_limit']} | Energy: {data['energy']}/{data['energy_limit']} | Coins: {data['coins']}")
        print("1. Jobs")
        print("2. Shop")
        print("3. Information")
        print("4. Sell Resources")
        print("0. Exit and Save")
        choice = input("Choose option: ")
        if choice == "1":
            jobs(data)
        elif choice == "2":
            shop(data)
        elif choice == "3":
            info(data)
        elif choice == "4":
            sell_resources(data)
        elif choice == "0":
            save_data(data)
            print("Game saved. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

# --- Jobs Menu ---
def jobs(data):
    while True:
        clear_screen()
        print("--- JOBS ---")
        print(f"Energy: {data['energy']}/{data['energy_limit']} | Coins: {data['coins']}")
        for k, v in MAPS.items():
            print(f"{k}. {v} - {MAP_DESCRIPTIONS[v]}")
        print("0. Back")
        choice = input("Choose a map: ")
        if choice == "0":
            return
        if choice not in MAPS:
            print("Invalid map choice.")
            continue
        if data['energy'] <= 0:
            print("No energy left! Buy chocolate loader in shop to restore energy.")
            input("Press Enter to continue...")
            return
        map_name = MAPS[choice]
        data['energy'] -= 1
        print(f"Mining in {map_name}...")
        if random.random() < 0.10:  # 10% chance
            item = random.choice(MAP_ITEMS[map_name])
            if item == "Unwanted Coins":
                coins_found = random.choice(ITEM_VALUES[item])
                data['coins'] += coins_found
                print(f"You found {coins_found} Unwanted Coins! Coins increased.")
            elif item == "Chocolate":
                data['items'][item] = data['items'].get(item, 0) + 1
                print(f"You found 1 Chocolate! Added to inventory.")
            elif item in ["Woods", "Leaves"]:
                data['items'][item] = data['items'].get(item, 0) + ITEM_VALUES[item]
                print(f"You found {ITEM_VALUES[item]} {item}! Added to inventory.")
            elif item in ["Shells", "Golds"]:
                data['items'][item] = data['items'].get(item, 0) + ITEM_VALUES[item]
                print(f"You found {ITEM_VALUES[item]} {item}! Added to inventory.")
        else:
            print("Please try again.")
        save_data(data)
        input("Press Enter to continue...")

# --- Shop Menu ---
def shop(data):
    while True:
        clear_screen()
        print("--- SHOP ---")
        print(f"Coins: {data['coins']}")
        for k, v in SHOP_ITEMS.items():
            animal_list = ', '.join(v['for'])
            print(f"{k}. {v['name']} ({v['price']} Coins) - For: {animal_list}")
        print("0. Back")
        choice = input("Choose item to buy: ")
        if choice == "0":
            return
        if choice not in SHOP_ITEMS:
            print("Invalid shop choice.")
            continue
        item = SHOP_ITEMS[choice]
        if data['coins'] < item['price']:
            print("Not enough coins!")
            input("Press Enter to continue...")
            continue
        if data['animal_type'] not in item['for']:
            print(f"{item['name']} cannot be used for {data['animal_type']}.")
            input("Press Enter to continue...")
            continue
        data['coins'] -= item['price']
        if item['name'] == "Loaders (Chocolate)":
            energy_gain = 10
            data['energy'] += energy_gain
            if data['energy'] > data['energy_limit']:
                data['energy'] = data['energy_limit']
            data['chocolates_used'] += 1
            print(f"Energy restored by {energy_gain}! ({data['energy']}/{data['energy_limit']})")
        else:
            data['foods'].append(item['name'])
            print(f"Bought {item['name']} for your {data['animal_name']} ({data['animal_type']}).")
            leveled_up = add_xp(data, 5)
            if leveled_up:
                print(f"{data['animal_name']} has leveled up!")
        save_data(data)
        input("Press Enter to continue...")

# --- Info Menu ---
def info(data):
    clear_screen()
    print("--- INFORMATION ---")
    print("\nMaps and Items:")
    for k, v in MAPS.items():
        items = ', '.join(MAP_ITEMS[v])
        print(f"- {v}: {items}\n  {MAP_DESCRIPTIONS[v]}")
    print("\nFoods for animals:")
    for k, v in ANIMALS.items():
        foods = []
        if v in SHOP_ITEMS["1"]["for"]:
            foods.append("Fresh fruits")
        if v in SHOP_ITEMS["2"]["for"]:
            foods.append("Raw meats")
        if v in SHOP_ITEMS["3"]["for"]:
            foods.append("Whole prey")
        print(f"- {v}: {', '.join(foods)}")
    print("\nYour items:")
    if not data["items"]:
        print("None")
    else:
        for item, qty in data["items"].items():
            print(f"{item}: {qty}")
    print("Foods bought:", ", ".join(data["foods"]) if data["foods"] else "None")
    print(f"Chocolates used for loaders: {data.get('chocolates_used', 0)}")
    print("\n0. Back")
    input("Press Enter to return...")

# --- Sell Resources ---
def sell_resources(data):
    clear_screen()
    print("--- SELL RESOURCES ---")
    print("You can sell Woods, Leaves, Shells, Golds for coins.")
    print("Current inventory:")
    for item in ["Woods", "Leaves", "Shells", "Golds"]:
        count = data["items"].get(item, 0)
        print(f"- {item}: {count}")
    print("0. Back")
    choice = input("Sell all available resources? (y/n): ").strip().lower()
    if choice == "0":
        return
    if choice != "y":
        print("Sell cancelled.")
        input("Press Enter to continue...")
        return
    total_earned = 0
    for item, (req_qty, earn) in ITEM_SELL_VALUES.items():
        qty = data["items"].get(item, 0)
        if qty >= req_qty:
            sell_times = qty // req_qty
            coins = earn * sell_times
            data["coins"] += coins
            data["items"][item] -= sell_times * req_qty
            total_earned += coins
    save_data(data)
    print(f"Sold resources. Total coins earned: {total_earned}")
    input("Press Enter to continue...")

# --- Main Program ---
def main():
    ensure_data()
    data = load_data()
    if not data.get("animal_type"):
        show_introduction()
        animal_type, animal_name = choose_animal()
        data["animal_type"] = animal_type
        data["animal_name"] = animal_name
        save_data(data)
    main_menu(data)

if __name__ == "__main__":
    main()
