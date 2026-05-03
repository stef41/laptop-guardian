# 🛡️ Laptop Guardian

**Anti-theft protection for your Mac.** Sits in your menu bar and locks your laptop when:

- 📶 **Bluetooth device disappears** — pair your phone, walk away and it locks
- 🔌 **USB device is unplugged** — attach a USB key as a "kill cord"
- ⚡ **Power adapter is yanked** — someone grabs your laptop off the table

## Install (one command)

```bash
pip install git+https://github.com/stef41/laptop-guardian.git
```

Or clone and install:

```bash
git clone https://github.com/stef41/laptop-guardian.git
cd laptop-guardian
pip install .
```

## Usage

```bash
laptop-guardian
```

A **🛡️** shield icon appears in your menu bar. Click it to:

1. **Configure your triggers** — set your Bluetooth device name, USB device, etc.
2. **Choose an action** — lock screen, sleep, or shutdown
3. **Arm Guardian** — click "Arm Guardian" when you're ready

When armed, the icon turns **🔴** and all monitors are active.

### Quick Setup

1. Run `laptop-guardian`
2. Click the shield → **Settings** → **BT Device** → type your phone name (e.g. "iPhone")
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
| **Sleep** | Mac goes to sleep |
| **Shutdown** | Mac shuts down |

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

- **macOS 12+** (Monterey or later)
- **Python 3.9+**

## How It Works

- Runs as a lightweight menu bar app using [rumps](https://github.com/jaredks/rumps)
- Bluetooth monitoring via `system_profiler SPBluetoothDataType`
- USB monitoring via `system_profiler SPUSBDataType`
- Power disconnect detection via `pmset`
- All monitors run in background threads with minimal CPU usage
- Triggers are only active when **armed** — no accidental locks during setup

## Uninstall

```bash
pip uninstall laptop-guardian
rm -rf ~/.config/laptop-guardian
```

## License

MIT
