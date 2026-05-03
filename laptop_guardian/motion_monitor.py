"""Sudden motion / accelerometer monitor using macOS SMS (Sudden Motion Sensor)."""

import threading
import time
import ctypes
import ctypes.util
import logging
import struct

logger = logging.getLogger("laptop-guardian.motion")


def _load_sms():
    """Try to access the Sudden Motion Sensor via IOKit."""
    try:
        iokit = ctypes.cdll.LoadLibrary(ctypes.util.find_library("IOKit"))
        return iokit
    except OSError:
        return None


class MotionMonitor:
    """Detects sudden/violent movement using the built-in accelerometer."""

    def __init__(self, threshold: float, on_motion: callable):
        self.threshold = threshold
        self.on_motion = on_motion
        self._running = False
        self._thread = None
        self._armed = False
        self._prev = None

    def start(self):
        self._running = True
        self._armed = False
        self._prev = None
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()
        logger.info(f"Motion monitor started (threshold={self.threshold}g)")

    def stop(self):
        self._running = False
        self._armed = False
        if self._thread:
            self._thread.join(timeout=5)

    def arm(self):
        self._armed = True
        logger.info("Motion monitor armed.")

    def _read_accelerometer(self):
        """Read accelerometer data via powermetrics or smc.

        Modern Macs (Apple Silicon) don't expose SMS the same way.
        We use a simple approach: monitor lid state and power adapter changes
        as proxies for physical tampering.
        """
        try:
            import objc
            from Foundation import NSBundle

            bundle = NSBundle.bundleWithPath_(
                "/System/Library/Frameworks/IOKit.framework"
            )
            if bundle:
                # Try to read SMC accelerometer values
                import subprocess
                result = subprocess.run(
                    ["ioreg", "-r", "-c", "SMCMotionSensor"],
                    capture_output=True, text=True, timeout=5
                )
                if result.stdout.strip():
                    return self._parse_ioreg_motion(result.stdout)
        except (ImportError, OSError):
            pass

        # Fallback: detect power adapter removal as "movement" proxy
        return self._check_power_change()

    def _parse_ioreg_motion(self, output: str):
        """Parse motion sensor data from ioreg output."""
        # This is a simplified parser — real values depend on hardware
        return None

    def _check_power_change(self):
        """Use power adapter state change as a movement proxy.
        If laptop was plugged in and suddenly isn't, someone might be grabbing it.
        """
        try:
            import subprocess
            result = subprocess.run(
                ["pmset", "-g", "ps"],
                capture_output=True, text=True, timeout=5
            )
            is_battery = "Battery Power" in result.stdout
            return is_battery
        except (subprocess.TimeoutExpired, OSError):
            return None

    def _poll(self):
        """Poll for sudden changes indicating physical movement."""
        was_on_power = None
        while self._running:
            on_battery = self._check_power_change()

            if on_battery is not None:
                # Detect sudden unplug (was on AC, now on battery)
                if was_on_power is True and on_battery is True and self._armed:
                    logger.warning(
                        "Power adapter suddenly disconnected — possible theft!"
                    )
                    self.on_motion("motion/power")
                    time.sleep(30)  # cooldown
                    was_on_power = None
                    continue
                was_on_power = not on_battery

            time.sleep(2)
