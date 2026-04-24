from pathlib import Path

import yaml

from models import Inventory


def load_inventory(path: str | Path) -> Inventory:
    data = yaml.safe_load(Path(path).read_text())
    return Inventory.model_validate(data)
