# 🛡️ Laptop Guardian

**Anti-theft protection for your laptop.** Sits in your system tray and locks your computer when:

<p align="center">
  <img src="demo.gif" alt="Laptop Guardian demo" width="800">
</p>

- 📶 **Bluetooth device disappears** — pair your phone, walk away and it locks
- 🔌 **USB device is unplugged** — attach a USB key as a "kill cord"
- ⚡ **Power adapter is yanked** — someone grabs your laptop off the table

Works on **macOS**, **Windows**, and **Linux**.

## Install

### macOS / Linux

**Copy-paste this into Terminal:**

```bash
curl -sL https://raw.githubusercontent.com/stef41/laptop-guardian/main/install.sh | bash
```

### Windows

1. [Download install.bat](https://raw.githubusercontent.com/stef41/laptop-guardian/main/install.bat)
2. Double-click it
3. If Python is missing, it opens the download page — install Python, then run `install.bat` again

That's it. The installer handles everything — Python, dependencies, shortcuts.

<details>
<summary>Alternative: install with pip (for developers)</summary>

```bash
pip install git+https://github.com/stef41/laptop-guardian.git
```

Or clone and install:

```bash
git clone https://github.com/stef41/laptop-guardian.git
cd laptop-guardian
pip install .
```
</details>

## Usage

```bash
laptop-guardian
```

A **shield icon** appears in your system tray. Right-click it to:

1. **Configure your triggers** — set your Bluetooth device name, USB device, etc.
2. **Choose an action** — lock screen, sleep, or shutdown
3. **Arm Guardian** — click "Arm Guardian" when you're ready

When armed, the icon turns **🔴** and all monitors are active.

### Quick Setup

1. Run `laptop-guardian`
2. Right-click the shield → **Settings** → **BT Device** → type your phone name (e.g. "iPhone")
3. Click **Arm Guardian**
4. Done! Your laptop locks when your phone goes out of Bluetooth range

### Triggers

| Trigger | What it detects | How to configure |
|---------|----------------|-----------------|
| **Bluetooth** | A paired device goes out of range | Set the device name in Settings |
| **USB** | A specific USB device is unplugged | Set the device name in Settings |
| **Motion/Power** | Power adapter is suddenly disconnected | Enabled by default, no config needed |

### Actions

| Action | What happens |
|--------|-------------|
| **Lock** (default) | Screen locks immediately |
| **Sleep** | Computer goes to sleep |
| **Shutdown** | Computer shuts down |

## Configuration

Settings are stored in `~/.config/laptop-guardian/config.json` and can be edited directly if preferred:

```json
{
  "bluetooth_enabled": true,
  "bluetooth_device": "iPhone",
  "bluetooth_timeout_sec": 10,
  "usb_enabled": true,
  "usb_device": "",
  "motion_enabled": true,
  "motion_threshold": 1.5,
  "lock_action": "lock",
  "alert_sound": true
}
```

## Requirements

- **macOS 12+**, **Windows 10+**, or **Linux** (with a system tray)
- **Python 3.9+** (the installer handles this for you)

## How It Works

- Runs as a lightweight system tray app using [pystray](https://github.com/moses-palmer/pystray)
- Bluetooth: `system_profiler` (macOS), `Get-PnpDevice` (Windows), `bluetoothctl` (Linux)
- USB: `system_profiler` (macOS), `Get-PnpDevice` (Windows), `lsusb` (Linux)
- Power disconnect detection via [psutil](https://github.com/giampaolo/psutil)
- All monitors run in background threads with minimal CPU usage
- Triggers are only active when **armed** — no accidental locks during setup

## Uninstall

**macOS / Linux:**
```bash
curl -sL https://raw.githubusercontent.com/stef41/laptop-guardian/main/uninstall.sh | bash
```

**Windows:** [Download uninstall.bat](https://raw.githubusercontent.com/stef41/laptop-guardian/main/uninstall.bat) and double-click it.

Or manually delete `~/.laptop-guardian` and `~/.config/laptop-guardian`.

## License

MIT
