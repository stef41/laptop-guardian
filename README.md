<div align="center">

# 🛡️ Laptop Guardian

### Your laptop locks itself the moment someone touches it.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)]()
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB.svg)](https://python.org)
[![GitHub release](https://img.shields.io/github/v/release/stef41/laptop-guardian)](https://github.com/stef41/laptop-guardian/releases)

[**Download**](https://stef41.github.io/laptop-guardian/) · [Report Bug](https://github.com/stef41/laptop-guardian/issues) · [Request Feature](https://github.com/stef41/laptop-guardian/issues)

<br/>

<img src="demo.gif" alt="Laptop Guardian demo" width="750">

<br/>

</div>

---

Laptop Guardian sits silently in your system tray. The moment your phone goes out of Bluetooth range, a USB device is unplugged, or your power cable is yanked — it **instantly locks your screen** (or sleeps / shuts down your machine).

No account. No cloud. No tracking. Just physics.

<br/>

## Why

You're at a coffee shop. You step away for 10 seconds. Someone grabs your laptop and walks out.

With Laptop Guardian armed, the moment the thief unplugs the charger or moves out of your phone's Bluetooth range, the screen locks. They get a locked machine. You get peace of mind.

<br/>

## Install

<table>
<tr>
<td width="33%" align="center"><h3>🍎 macOS</h3></td>
<td width="33%" align="center"><h3>🪟 Windows</h3></td>
<td width="33%" align="center"><h3>🐧 Linux</h3></td>
</tr>
<tr>
<td align="center">

[**Download .app**](https://github.com/stef41/laptop-guardian/releases/latest/download/LaptopGuardian-mac.zip)

Unzip → double-click → done.
</td>
<td align="center">

[**Download installer**](https://github.com/stef41/laptop-guardian/releases/latest/download/LaptopGuardian-windows-installer.bat)

Double-click → installs everything.
</td>
<td align="center">

```bash
curl -sL https://raw.githubusercontent.com/stef41/laptop-guardian/main/install.sh | bash
```
</td>
</tr>
</table>

> **No terminal, no pip, no git.** The installer handles Python, dependencies, and creates app shortcuts automatically. [More install options →](#advanced-install)

<br/>

## How It Works

```
You sit down at a café → Open Laptop Guardian → Set your phone as trusted device → Click "Arm"
                                                                                      ↓
                                              🛡️ shield icon turns 🔴 — your laptop is protected
                                                                                      ↓
                         Someone grabs your laptop / you walk away with your phone → 🔒 LOCKED
```

1. **Download & open** — a shield icon appears in your system tray
2. **Set your phone name** — right-click → Settings → BT Device → `"iPhone"` or `"Galaxy S24"`
3. **Arm it** — click `Arm Guardian` — the shield turns red
4. **That's it** — walk away with your phone, laptop locks in ~10 seconds

<br/>

## Triggers

| Trigger | What happens | Use case |
|---|---|---|
| **📶 Bluetooth** | Locks when a paired device goes out of range (~10m) | Keep your phone in your pocket — walk away and it locks |
| **🔌 USB kill cord** | Locks when a specific USB device is disconnected | Attach a cheap USB key to your wrist — if someone grabs the laptop, it yanks out |
| **⚡ Power yank** | Locks when the charger is suddenly disconnected | Laptop is plugged in on a table — someone grabs it and runs |

All triggers are independently toggleable. Use one, two, or all three.

<br/>

## Actions

When a trigger fires, Laptop Guardian can:

| Action | Description |
|---|---|
| 🔒 **Lock** (default) | Locks the screen immediately |
| 😴 **Sleep** | Puts the machine to sleep |
| ⚠️ **Shutdown** | Shuts down the machine |
| 🔊 **Alarm** | Plays an alert sound (optional, on by default) |

<br/>

## Configuration

Everything is configurable from the tray menu — no config files needed.

<details>
<summary>Power users: edit <code>~/.config/laptop-guardian/config.json</code> directly</summary>

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

</details>

<br/>

## Platform Support

Laptop Guardian uses native OS commands under the hood — no elevated permissions required for basic operation.

| Component | macOS | Windows | Linux |
|---|:---:|:---:|:---:|
| System tray | ✅ | ✅ | ✅ |
| Bluetooth proximity | ✅ `system_profiler` | ✅ `Get-PnpDevice` | ✅ `bluetoothctl` |
| USB disconnect | ✅ `system_profiler` | ✅ `Get-PnpDevice` | ✅ `lsusb` |
| Power yank detection | ✅ `psutil` | ✅ `psutil` | ✅ `psutil` |
| Lock screen | ✅ `pmset` | ✅ `rundll32` | ✅ `loginctl` |
| Sleep | ✅ | ✅ | ✅ |
| Shutdown | ✅ | ✅ | ✅ |

<br/>

## Architecture

```
┌─────────────────────────────────────────┐
│              System Tray UI             │  ← pystray + tkinter
│         (arm / disarm / settings)       │
├─────────────────────────────────────────┤
│          Monitor Threads (daemon)       │
│  ┌─────────┐ ┌──────┐ ┌─────────────┐  │
│  │Bluetooth│ │ USB  │ │ Power/Motion│  │  ← background polling
│  └────┬────┘ └──┬───┘ └──────┬──────┘  │
│       └─────────┴────────────┘          │
│                  ↓                      │
│           Trigger Engine                │  ← cooldown, dedup
│                  ↓                      │
│         Action Executor                 │  ← lock / sleep / shutdown + alarm
└─────────────────────────────────────────┘
```

- **~0% CPU** at idle — monitors poll every 2-3 seconds using lightweight OS commands
- **No network access** — everything runs locally, no telemetry, no cloud
- **No root/admin** — works with standard user permissions
- **Arm/disarm model** — triggers only fire when explicitly armed, preventing false locks during setup

<br/>

## Advanced Install

<details>
<summary><strong>pip install (developers)</strong></summary>

```bash
pip install git+https://github.com/stef41/laptop-guardian.git
laptop-guardian
```
</details>

<details>
<summary><strong>From source</strong></summary>

```bash
git clone https://github.com/stef41/laptop-guardian.git
cd laptop-guardian
pip install .
laptop-guardian
```
</details>

<br/>

## Uninstall

<table>
<tr><td>🍎 macOS / 🐧 Linux</td><td>

```bash
curl -sL https://raw.githubusercontent.com/stef41/laptop-guardian/main/uninstall.sh | bash
```
</td></tr>
<tr><td>🪟 Windows</td><td>

[Download uninstall.bat](https://raw.githubusercontent.com/stef41/laptop-guardian/main/uninstall.bat) and double-click.
</td></tr>
</table>

<br/>

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

<br/>

## License

[MIT](LICENSE) — use it however you want.
