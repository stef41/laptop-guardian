"""USB device disconnect monitor — cross-platform."""

import threading
import time
import subprocess
import platform
import logging

logger = logging.getLogger("laptop-guardian.usb")
SYSTEM = platform.system()


class USBMonitor:
    """Monitors for USB device disconnection and triggers callback."""

    def __init__(self, device_name: str, on_disconnect: callable):
        self.device_name = device_name
        self.on_disconnect = on_disconnect
        self._running = False
        self._thread = None
        self._armed = False
        self._was_connected = False

    def start(self):
        if not self.device_name:
            logger.warning("No USB device configured, skipping.")
            return
        self._running = True
        self._armed = False
        self._was_connected = False
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()
        logger.info(f"USB monitor started, watching for '{self.device_name}'")

    def stop(self):
        self._running = False
        self._armed = False
        if self._thread:
            self._thread.join(timeout=5)

    def arm(self):
        self._armed = True
        self._was_connected = self._is_device_present()
        logger.info("USB monitor armed.")

    def _is_device_present(self) -> bool:
        """Check if the USB device is present via OS-specific methods."""
        try:
            if SYSTEM == "Darwin":
                result = subprocess.run(
                    ["system_profiler", "SPUSBDataType"],
                    capture_output=True, text=True, timeout=10
                )
            elif SYSTEM == "Windows":
                result = subprocess.run(
                    ["powershell", "-c",
                     "Get-PnpDevice -Class USB | "
                     "Where-Object { $_.Status -eq 'OK' } | "
                     "Select-Object -ExpandProperty FriendlyName"],
                    capture_output=True, text=True, timeout=10
                )
            else:  # Linux
                result = subprocess.run(
                    ["lsusb"],
                    capture_output=True, text=True, timeout=10
                )
            return self.device_name.lower() in result.stdout.lower()
        except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
            return False

    def _poll(self):
        while self._running:
            present = self._is_device_present()
            if present:
                self._was_connected = True
            elif self._was_connected and self._armed:
                logger.warning("USB device disconnected! Triggering action.")
                self.on_disconnect("usb")
                self._was_connected = False
                time.sleep(30)
                continue
            time.sleep(2)
