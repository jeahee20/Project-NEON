DEBUG_LOADER = False
import json
import os
import random


DIALOGUE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "dialogues"
)


def _dialogue_path(category):
    return os.path.join(DIALOGUE_DIR, f"{category}.json")


def load_dialogues(category):
    path = _dialogue_path(category)
    if DEBUG_LOADER:
        print("[LOADER] dir:", DIALOGUE_DIR)

    if not os.path.exists(path):
        if DEBUG_LOADER:
            print(f"[LOADER] missing {category}.json : 0 entries")
        return []

    with open(path, "r", encoding="utf-8") as file:
        dialogues = json.load(file)

    if DEBUG_LOADER:
        print(f"[LOADER] loaded {category}.json : {len(dialogues)} entries")
    return dialogues


def load_all_dialogues():
    dialogues = {}

    if not os.path.isdir(DIALOGUE_DIR):
        return dialogues

    for filename in os.listdir(DIALOGUE_DIR):
        if not filename.endswith(".json"):
            continue

        category = filename[:-5]
        dialogues[category] = load_dialogues(category)

    return dialogues


def get_examples(category, limit=5):
    dialogues = load_dialogues(category)

    if limit is None or limit >= len(dialogues):
        return dialogues

    return random.sample(dialogues, limit)


def get_forbidden_phrases():
    return load_dialogues("forbidden")
