"""STUB: returns one fake change. Replaced by the real parser."""
from .models import SettingChange


def parse_settings(path, text):
    return {}


def find_changes(base, head, watched, cwd="."):
    return [SettingChange(key="train.lr", old="0.001", new="0.0005", file="configs/train.yaml")]
