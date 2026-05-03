# Laptop Guardian — Demo
# https://github.com/stef41/laptop-guardian

Output demo.gif
Set Shell bash
Set FontSize 16
Set Width 900
Set Height 500
Set Theme "Catppuccin Mocha"
Set Padding 20
Set TypingSpeed 40ms
Set WindowBar Colorful
Set WindowBarSize 40

# Title
Type "# 🛡️ Laptop Guardian — Anti-theft for macOS"
Enter
Sleep 1.5s

# Show install command
Type "curl -sL https://raw.githubusercontent.com/stef41/laptop-guardian/main/install.sh | bash"
Sleep 1s
Enter
Sleep 1s

# Simulate install output
Type@0 ""
Sleep 300ms
Type@0 "🛡️  Installing Laptop Guardian..."
Enter
Sleep 500ms
Type@0 ""
Enter
Type@0 "   Python: Python 3.12.4"
Enter
Sleep 300ms
Type@0 "📁 Creating environment in /Users/you/.laptop-guardian..."
Enter
Sleep 500ms
Type@0 "⬇️  Installing laptop-guardian..."
Enter
Sleep 1.5s
Type@0 "   Installed: Version: 1.0.0"
Enter
Sleep 300ms
Type@0 "🖥️  Creating app in ~/Applications..."
Enter
Sleep 500ms
Type@0 ""
Enter
Type@0 "✅ Laptop Guardian installed!"
Enter
Type@0 ""
Enter
Type@0 "   How to launch:"
Enter
Type@0 "   • Open '~/Applications/Laptop Guardian' (double-click)"
Enter
Type@0 "   • Or Spotlight: press ⌘+Space, type 'Laptop Guardian'"
Enter
Type@0 "   • Or terminal: laptop-guardian"
Enter
Type@0 ""
Enter
Type@0 "   A 🛡️ icon will appear in your menu bar."
Enter
Type@0 "   Click it → set your phone name → click 'Arm Guardian'."
Enter

Sleep 2s

# Launch the app
Type ""
Enter
Type "# Now let's launch it!"
Enter
Sleep 1s
Type "laptop-guardian &"
Enter
Sleep 1s
Type@0 "🛡️ Laptop Guardian running in menu bar"
Enter

Sleep 2s

# Show config
Type ""
Enter
Type "# Your config lives here:"
Enter
Sleep 500ms
Type "cat ~/.config/laptop-guardian/config.json"
Enter
Sleep 500ms

Type@0 '{'
Enter
Type@0 '  "bluetooth_enabled": true,'
Enter
Type@0 '  "bluetooth_device": "iPhone",'
Enter
Type@0 '  "bluetooth_timeout_sec": 10,'
Enter
Type@0 '  "usb_enabled": true,'
Enter
Type@0 '  "usb_device": "",'
Enter
Type@0 '  "motion_enabled": true,'
Enter
Type@0 '  "lock_action": "lock",'
Enter
Type@0 '  "alert_sound": true'
Enter
Type@0 '}'
Enter

Sleep 2s

# Menu bar walkthrough
Type ""
Enter
Type "# Click 🛡️ in menu bar → Arm Guardian → 🔴 Armed!"
Enter
Type "# Your laptop is now protected."
Enter
Sleep 1s
Type ""
Enter
Type "# Walk away with your phone → laptop locks automatically 🔒"
Enter

Sleep 3s
