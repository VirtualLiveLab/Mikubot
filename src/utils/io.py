import json
from pathlib import Path
from typing import Any


def get_cwd() -> Path:
    return Path.cwd()


def read_json(filename: str) -> dict[str, Any]:
    path = get_cwd() / filename
    with path.open(mode="r") as f:
        return json.load(f)
