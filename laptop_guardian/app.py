"""Laptop Guardian — macOS menu bar app."""

import logging
import rumps
from laptop_guardian.config import load_config, save_config, DEFAULTS
from laptop_guardian.actions import execute_action
from laptop_guardian.bluetooth_monitor import BluetoothMonitor
from laptop_guardian.usb_monitor import USBMonitor
from laptop_guardian.motion_monitor import MotionMonitor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("laptop-guardian")


class LaptopGuardianApp(rumps.App):
    def __init__(self):
        super().__init__(
            "Laptop Guardian",
            icon=None,
            title="🛡️",
            quit_button=None,
        )
        self.config = load_config()
        self.monitors = []
        self._armed = False

        # Build menu
        self.arm_button = rumps.MenuItem("Arm Guardian", callback=self.toggle_arm)
        self.status_item = rumps.MenuItem("Status: Disarmed")
        self.status_item.set_callback(None)

        # Settings submenu
        settings_menu = rumps.MenuItem("Settings")

        self.bt_toggle = rumps.MenuItem(
            f"Bluetooth: {'ON' if self.config['bluetooth_enabled'] else 'OFF'}",
            callback=self.toggle_bluetooth,
        )
        self.bt_device = rumps.MenuItem(
            f"BT Device: {self.config['bluetooth_device'] or 'Not Set'}",
            callback=self.set_bluetooth_device,
        )
        self.usb_toggle = rumps.MenuItem(
            f"USB Watch: {'ON' if self.config['usb_enabled'] else 'OFF'}",
            callback=self.toggle_usb,
        )
        self.usb_device = rumps.MenuItem(
            f"USB Device: {self.config['usb_device'] or 'Not Set'}",
            callback=self.set_usb_device,
        )
        self.motion_toggle = rumps.MenuItem(
            f"Motion/Power: {'ON' if self.config['motion_enabled'] else 'OFF'}",
            callback=self.toggle_motion,
        )
        self.action_item = rumps.MenuItem(
            f"Action: {self.config['lock_action'].title()}",
            callback=self.set_action,
        )
        self.sound_toggle = rumps.MenuItem(
            f"Alert Sound: {'ON' if self.config['alert_sound'] else 'OFF'}",
            callback=self.toggle_sound,
        )

        settings_menu.update([
            self.bt_toggle,
            self.bt_device,
            None,  # separator
            self.usb_toggle,
            self.usb_device,
            None,
            self.motion_toggle,
            None,
            self.action_item,
            self.sound_toggle,
        ])

        self.menu = [
            self.arm_button,
            self.status_item,
            None,
            settings_menu,
            None,
            rumps.MenuItem("Quit", callback=self.quit_app),
        ]

    def toggle_arm(self, sender):
        if self._armed:
            self._disarm()
        else:
            self._arm()

    def _arm(self):
        self._armed = True
        self.arm_button.title = "Disarm Guardian"
        self.status_item.title = "Status: 🔴 ARMED"
        self.title = "🔴"
        self._start_monitors()
        rumps.notification(
            "Laptop Guardian",
            "Armed",
            "All configured monitors are active. Your laptop is protected.",
        )

    def _disarm(self):
        self._armed = False
        self.arm_button.title = "Arm Guardian"
        self.status_item.title = "Status: Disarmed"
        self.title = "🛡️"
        self._stop_monitors()
        rumps.notification("Laptop Guardian", "Disarmed", "Protection disabled.")

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
        # Auto-disarm after trigger to prevent loops
        self._disarm()

    # --- Settings callbacks ---

    def toggle_bluetooth(self, sender):
        self.config["bluetooth_enabled"] = not self.config["bluetooth_enabled"]
        sender.title = f"Bluetooth: {'ON' if self.config['bluetooth_enabled'] else 'OFF'}"
        save_config(self.config)

    def set_bluetooth_device(self, sender):
        response = rumps.Window(
            message="Enter the name of your trusted Bluetooth device\n"
                    "(e.g., your phone name as shown in Bluetooth settings):",
            title="Bluetooth Device",
            default_text=self.config["bluetooth_device"],
            ok="Save",
            cancel="Cancel",
        ).run()
        if response.clicked:
            self.config["bluetooth_device"] = response.text.strip()
            sender.title = f"BT Device: {self.config['bluetooth_device'] or 'Not Set'}"
            save_config(self.config)

    def toggle_usb(self, sender):
        self.config["usb_enabled"] = not self.config["usb_enabled"]
        sender.title = f"USB Watch: {'ON' if self.config['usb_enabled'] else 'OFF'}"
        save_config(self.config)

    def set_usb_device(self, sender):
        response = rumps.Window(
            message="Enter the name of your USB device to watch\n"
                    "(e.g., a USB key name — check System Information > USB):",
            title="USB Device",
            default_text=self.config["usb_device"],
            ok="Save",
            cancel="Cancel",
        ).run()
        if response.clicked:
            self.config["usb_device"] = response.text.strip()
            sender.title = f"USB Device: {self.config['usb_device'] or 'Not Set'}"
            save_config(self.config)

    def toggle_motion(self, sender):
        self.config["motion_enabled"] = not self.config["motion_enabled"]
        sender.title = f"Motion/Power: {'ON' if self.config['motion_enabled'] else 'OFF'}"
        save_config(self.config)

    def set_action(self, sender):
        response = rumps.Window(
            message="Choose action when triggered:\n"
                    "  • lock — Lock the screen\n"
                    "  • sleep — Put Mac to sleep\n"
                    "  • shutdown — Shut down the Mac",
            title="Trigger Action",
            default_text=self.config["lock_action"],
            ok="Save",
            cancel="Cancel",
        ).run()
        if response.clicked:
            val = response.text.strip().lower()
            if val in ("lock", "sleep", "shutdown"):
                self.config["lock_action"] = val
                sender.title = f"Action: {val.title()}"
                save_config(self.config)

    def toggle_sound(self, sender):
        self.config["alert_sound"] = not self.config["alert_sound"]
        sender.title = f"Alert Sound: {'ON' if self.config['alert_sound'] else 'OFF'}"
        save_config(self.config)

    def quit_app(self, sender):
        self._stop_monitors()
        rumps.quit_application()


def main():
    LaptopGuardianApp().run()


if __name__ == "__main__":
    main()
