"""Configuration management for Laptop Guardian."""

import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "laptop-guardian"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "bluetooth_enabled": True,
    "bluetooth_device": "",          # MAC address or name of trusted device
    "bluetooth_timeout_sec": 10,     # seconds before triggering lock
    "usb_enabled": True,
    "usb_device": "",                # device name or serial to watch
    "motion_enabled": True,
    "motion_threshold": 1.5,         # g-force threshold
    "lock_action": "lock",           # "lock" | "sleep" | "shutdown"
    "alert_sound": True,
    "launch_at_login": False,
}


def load_config() -> dict:
    """Load config from disk, merging with defaults."""
    config = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                saved = json.load(f)
            config.update(saved)
        except (json.JSONDecodeError, OSError):
            pass
    return config


def save_config(config: dict) -> None:
    """Persist config to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
