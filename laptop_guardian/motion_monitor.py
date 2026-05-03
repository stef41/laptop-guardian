"""Power disconnect / motion monitor — cross-platform via psutil."""

import threading
import time
import logging

logger = logging.getLogger("laptop-guardian.motion")


class MotionMonitor:
    """Detects sudden power adapter disconnection (theft proxy) using psutil."""

    def __init__(self, threshold: float, on_motion: callable):
        self.threshold = threshold
        self.on_motion = on_motion
        self._running = False
        self._thread = None
        self._armed = False

    def start(self):
        self._running = True
        self._armed = False
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()
        logger.info("Power/motion monitor started")

    def stop(self):
        self._running = False
        self._armed = False
        if self._thread:
            self._thread.join(timeout=5)

    def arm(self):
        self._armed = True
        logger.info("Power/motion monitor armed.")

    def _is_on_ac_power(self) -> bool | None:
        """Check if plugged into AC power. Returns None if no battery."""
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery is None:
                return None  # desktop, no battery
            return battery.power_plugged
        except (ImportError, AttributeError):
            return None

    def _poll(self):
        was_on_power = None
        while self._running:
            on_ac = self._is_on_ac_power()
            if on_ac is None:
                # No battery sensor — nothing to monitor
                time.sleep(10)
                continue

            if was_on_power is True and on_ac is False and self._armed:
                logger.warning(
                    "Power adapter suddenly disconnected — possible theft!"
                )
                self.on_motion("motion/power")
                time.sleep(30)  # cooldown
                was_on_power = None
                continue

            was_on_power = on_ac
            time.sleep(2)
