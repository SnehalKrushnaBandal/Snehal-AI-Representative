import json
from pathlib import Path


def load_candidate_profile(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
