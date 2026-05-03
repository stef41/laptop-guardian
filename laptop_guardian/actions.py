"""Lock actions — what happens when a trigger fires."""

import subprocess
import platform


def lock_screen():
    """Lock the screen (macOS)."""
    subprocess.Popen([
        "/usr/bin/pmset", "displaysleepnow"
    ])


def sleep_machine():
    """Put the machine to sleep."""
    subprocess.Popen([
        "/usr/bin/pmset", "sleepnow"
    ])


def shutdown_machine():
    """Shut down immediately."""
    subprocess.Popen([
        "/usr/bin/osascript", "-e",
        'tell application "System Events" to shut down'
    ])


def play_alarm():
    """Play a loud alarm sound."""
    # Use macOS 'afplay' with the built-in alarm sound
    alarm_path = "/System/Library/Sounds/Sosumi.aiff"
    # Play it 5 times rapidly for attention
    subprocess.Popen([
        "/usr/bin/afplay", alarm_path
    ])


ACTIONS = {
    "lock": lock_screen,
    "sleep": sleep_machine,
    "shutdown": shutdown_machine,
}


def execute_action(action_name: str, alert_sound: bool = True):
    """Execute the configured lock action."""
    if alert_sound:
        play_alarm()
    fn = ACTIONS.get(action_name, lock_screen)
    fn()
