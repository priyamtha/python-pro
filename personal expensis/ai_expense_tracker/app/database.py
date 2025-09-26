import json
import os

JSON_FILE = "data/expenses.json"
os.makedirs("data", exist_ok=True)

# Initialize JSON if not exists
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w") as f:
        json.dump([], f)

def load_expenses():
    with open(JSON_FILE, "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(JSON_FILE, "w") as f:
        json.dump(expenses, f, indent=4)
