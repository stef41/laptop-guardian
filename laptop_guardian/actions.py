"""Lock actions — what happens when a trigger fires."""

import subprocess
import sys
import platform

SYSTEM = platform.system()


def lock_screen():
    """Lock the screen."""
    if SYSTEM == "Darwin":
        subprocess.Popen(["/usr/bin/pmset", "displaysleepnow"])
    elif SYSTEM == "Windows":
        subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"])
    else:  # Linux
        # Try common lockers in order
        for cmd in [
            ["loginctl", "lock-session"],
            ["xdg-screensaver", "lock"],
            ["gnome-screensaver-command", "-l"],
            ["xscreensaver-command", "-lock"],
        ]:
            try:
                subprocess.Popen(cmd)
                return
            except FileNotFoundError:
                continue


def sleep_machine():
    """Put the machine to sleep."""
    if SYSTEM == "Darwin":
        subprocess.Popen(["/usr/bin/pmset", "sleepnow"])
    elif SYSTEM == "Windows":
        subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
    else:
        subprocess.Popen(["systemctl", "suspend"])


def shutdown_machine():
    """Shut down immediately."""
    if SYSTEM == "Darwin":
        subprocess.Popen([
            "/usr/bin/osascript", "-e",
            'tell application "System Events" to shut down'
        ])
    elif SYSTEM == "Windows":
        subprocess.Popen(["shutdown", "/s", "/t", "0"])
    else:
        subprocess.Popen(["systemctl", "poweroff"])


def play_alarm():
    """Play a loud alarm sound."""
    if SYSTEM == "Darwin":
        alarm_path = "/System/Library/Sounds/Sosumi.aiff"
        subprocess.Popen(["/usr/bin/afplay", alarm_path])
    elif SYSTEM == "Windows":
        # Use PowerShell to beep
        subprocess.Popen([
            "powershell", "-c",
            "[console]::beep(1000,1500)"
        ])
    else:
        # Try paplay or aplay
        for cmd in [
            ["paplay", "/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga"],
            ["aplay", "/usr/share/sounds/alsa/Front_Center.wav"],
        ]:
            try:
                subprocess.Popen(cmd)
                return
            except FileNotFoundError:
                continue


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
