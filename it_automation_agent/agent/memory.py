import json
import os

# ✅ Save inside agent folder
FILE_PATH = os.path.join(os.path.dirname(__file__), "agent_memory.json")


def load_memory():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    return {"actions_taken": []}


def save_memory(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)


def add_action(action):
    data = load_memory()
    data["actions_taken"].append(action)
    save_memory(data)


def get_actions():
    data = load_memory()
    return data["actions_taken"]