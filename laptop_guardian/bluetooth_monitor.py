"""Bluetooth proximity monitor using CoreBluetooth."""

import threading
import time
import subprocess
import logging

logger = logging.getLogger("laptop-guardian.bluetooth")


class BluetoothMonitor:
    """Monitors a paired Bluetooth device and triggers callback when it disappears."""

    def __init__(self, device_name: str, timeout_sec: int, on_lost: callable):
        self.device_name = device_name
        self.timeout_sec = timeout_sec
        self.on_lost = on_lost
        self._running = False
        self._thread = None
        self._armed = False

    def start(self):
        if not self.device_name:
            logger.warning("No Bluetooth device configured, skipping.")
            return
        self._running = True
        self._armed = False
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()
        logger.info(f"Bluetooth monitor started, watching for '{self.device_name}'")

    def stop(self):
        self._running = False
        self._armed = False
        if self._thread:
            self._thread.join(timeout=5)

    def arm(self):
        """Arm the monitor — only triggers after armed (so setup doesn't false-fire)."""
        self._armed = True
        logger.info("Bluetooth monitor armed.")

    def _is_device_connected(self) -> bool:
        """Check if the device is connected via system_profiler."""
        try:
            result = subprocess.run(
                ["system_profiler", "SPBluetoothDataType"],
                capture_output=True, text=True, timeout=10
            )
            return self.device_name.lower() in result.stdout.lower()
        except (subprocess.TimeoutExpired, OSError):
            return False

    def _poll(self):
        lost_since = None
        while self._running:
            connected = self._is_device_connected()
            if connected:
                lost_since = None
            else:
                if lost_since is None:
                    lost_since = time.time()
                    logger.info(f"Bluetooth device '{self.device_name}' not found...")
                elif self._armed and (time.time() - lost_since) >= self.timeout_sec:
                    logger.warning("Bluetooth device lost! Triggering action.")
                    self.on_lost("bluetooth")
                    lost_since = None  # reset after trigger
                    time.sleep(30)     # cooldown
                    continue
            time.sleep(3)
