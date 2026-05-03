"""Laptop Guardian — cross-platform system tray app."""

import logging
import platform
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageDraw
import pystray

from laptop_guardian.config import load_config, save_config
from laptop_guardian.actions import execute_action
from laptop_guardian.bluetooth_monitor import BluetoothMonitor
from laptop_guardian.usb_monitor import USBMonitor
from laptop_guardian.motion_monitor import MotionMonitor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("laptop-guardian")

SYSTEM = platform.system()


def _create_icon_image(armed: bool) -> Image.Image:
    """Create a simple tray icon — green shield (disarmed) or red (armed)."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    color = (220, 40, 40, 255) if armed else (60, 160, 80, 255)
    # Shield shape
    draw.polygon([
        (32, 4), (58, 16), (54, 44), (32, 60), (10, 44), (6, 16)
    ], fill=color, outline=(255, 255, 255, 200))
    # Inner highlight
    draw.polygon([
        (32, 12), (48, 20), (46, 40), (32, 50), (18, 40), (16, 20)
    ], fill=(255, 255, 255, 60))
    return img


def _tk_prompt(title: str, message: str, default: str = "") -> str | None:
    """Show a tkinter input dialog (works cross-platform)."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    result = simpledialog.askstring(title, message, initialvalue=default, parent=root)
    root.destroy()
    return result


def _tk_info(title: str, message: str):
    """Show an info popup."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo(title, message, parent=root)
    root.destroy()


class LaptopGuardianApp:
    def __init__(self):
        self.config = load_config()
        self.monitors: list = []
        self._armed = False
        self._icon: pystray.Icon | None = None

    def _build_menu(self) -> pystray.Menu:
        return pystray.Menu(
            pystray.MenuItem(
                "Disarm Guardian" if self._armed else "Arm Guardian",
                self._toggle_arm,
                default=True,
            ),
            pystray.MenuItem(
                f"Status: {'🔴 ARMED' if self._armed else 'Disarmed'}",
                None,
                enabled=False,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Settings", pystray.Menu(
                pystray.MenuItem(
                    f"Bluetooth: {'ON' if self.config['bluetooth_enabled'] else 'OFF'}",
                    self._toggle_bluetooth,
                ),
                pystray.MenuItem(
                    f"BT Device: {self.config['bluetooth_device'] or 'Not Set'}",
                    self._set_bluetooth_device,
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(
                    f"USB Watch: {'ON' if self.config['usb_enabled'] else 'OFF'}",
                    self._toggle_usb,
                ),
                pystray.MenuItem(
                    f"USB Device: {self.config['usb_device'] or 'Not Set'}",
                    self._set_usb_device,
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(
                    f"Power Yank: {'ON' if self.config['motion_enabled'] else 'OFF'}",
                    self._toggle_motion,
                ),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(
                    f"Action: {self.config['lock_action'].title()}",
                    self._set_action,
                ),
                pystray.MenuItem(
                    f"Alert Sound: {'ON' if self.config['alert_sound'] else 'OFF'}",
                    self._toggle_sound,
                ),
            )),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._quit),
        )

    def _refresh_menu(self):
        if self._icon:
            self._icon.menu = self._build_menu()
            self._icon.icon = _create_icon_image(self._armed)

    # ── Arm / Disarm ──────────────────────────────────────────────

    def _toggle_arm(self, icon, item):
        if self._armed:
            self._disarm()
        else:
            self._arm()

    def _arm(self):
        self._armed = True
        self._start_monitors()
        self._refresh_menu()
        logger.info("Guardian ARMED")

    def _disarm(self):
        self._armed = False
        self._stop_monitors()
        self._refresh_menu()
        logger.info("Guardian disarmed")

    def _start_monitors(self):
        self._stop_monitors()

        if self.config["bluetooth_enabled"] and self.config["bluetooth_device"]:
            bt = BluetoothMonitor(
                self.config["bluetooth_device"],
                self.config["bluetooth_timeout_sec"],
                self._trigger,
            )
            bt.start()
            bt.arm()
            self.monitors.append(bt)

        if self.config["usb_enabled"] and self.config["usb_device"]:
            usb = USBMonitor(self.config["usb_device"], self._trigger)
            usb.start()
            usb.arm()
            self.monitors.append(usb)

        if self.config["motion_enabled"]:
            motion = MotionMonitor(self.config["motion_threshold"], self._trigger)
            motion.start()
            motion.arm()
            self.monitors.append(motion)

    def _stop_monitors(self):
        for m in self.monitors:
            m.stop()
        self.monitors.clear()

    def _trigger(self, source: str):
        logger.warning(f"TRIGGER from {source}!")
        execute_action(self.config["lock_action"], self.config["alert_sound"])
        self._disarm()

    # ── Settings callbacks ────────────────────────────────────────

    def _toggle_bluetooth(self, icon, item):
        self.config["bluetooth_enabled"] = not self.config["bluetooth_enabled"]
        save_config(self.config)
        self._refresh_menu()

    def _set_bluetooth_device(self, icon, item):
        result = _tk_prompt(
            "Bluetooth Device",
            "Enter your trusted Bluetooth device name\n"
            "(e.g. your phone name from Bluetooth settings):",
            self.config["bluetooth_device"],
        )
        if result is not None:
            self.config["bluetooth_device"] = result.strip()
            save_config(self.config)
            self._refresh_menu()

    def _toggle_usb(self, icon, item):
        self.config["usb_enabled"] = not self.config["usb_enabled"]
        save_config(self.config)
        self._refresh_menu()

    def _set_usb_device(self, icon, item):
        hint = {
            "Darwin": "System Information → USB",
            "Windows": "Device Manager → USB",
            "Linux": "run 'lsusb' in terminal",
        }.get(SYSTEM, "your OS device manager")
        result = _tk_prompt(
            "USB Device",
            f"Enter the USB device name to watch\n(check {hint}):",
            self.config["usb_device"],
        )
        if result is not None:
            self.config["usb_device"] = result.strip()
            save_config(self.config)
            self._refresh_menu()

    def _toggle_motion(self, icon, item):
        self.config["motion_enabled"] = not self.config["motion_enabled"]
        save_config(self.config)
        self._refresh_menu()

    def _set_action(self, icon, item):
        result = _tk_prompt(
            "Trigger Action",
            "Type one of: lock, sleep, shutdown",
            self.config["lock_action"],
        )
        if result and result.strip().lower() in ("lock", "sleep", "shutdown"):
            self.config["lock_action"] = result.strip().lower()
            save_config(self.config)
            self._refresh_menu()

    def _toggle_sound(self, icon, item):
        self.config["alert_sound"] = not self.config["alert_sound"]
        save_config(self.config)
        self._refresh_menu()

    def _quit(self, icon, item):
        self._stop_monitors()
        icon.stop()

    def run(self):
        self._icon = pystray.Icon(
            "laptop-guardian",
            icon=_create_icon_image(False),
            title="Laptop Guardian",
            menu=self._build_menu(),
        )
        self._icon.run()


def main():
    LaptopGuardianApp().run()


if __name__ == "__main__":
    main()
