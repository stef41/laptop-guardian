#!/bin/bash
# Laptop Guardian — one-command installer for macOS / Linux
# Usage: curl -sL https://raw.githubusercontent.com/stef41/laptop-guardian/main/install.sh | bash
set -e

echo ""
echo "🛡️  Installing Laptop Guardian..."
echo ""

# ── 1. Ensure Python 3 is available ─────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "🐍 Python 3 not found. Installing..."
    if command -v brew &>/dev/null; then
        brew install python
    elif command -v apt-get &>/dev/null; then
        sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip python3-tk
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 python3-tkinter
    elif command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm python tk
    else
        echo "❌ Could not install Python 3. Please install it manually."
        exit 1
    fi
fi

# Linux: ensure tkinter is available
if [[ "$(uname)" == "Linux" ]]; then
    python3 -c "import tkinter" 2>/dev/null || {
        echo "📦 Installing tkinter..."
        if command -v apt-get &>/dev/null; then
            sudo apt-get install -y python3-tk
        elif command -v dnf &>/dev/null; then
            sudo dnf install -y python3-tkinter
        elif command -v pacman &>/dev/null; then
            sudo pacman -S --noconfirm tk
        fi
    }
fi

echo "   Python: $(python3 --version)"

INSTALL_DIR="$HOME/.laptop-guardian"

# ── 2. Create isolated virtual environment ──────────────────────
if [[ -d "$INSTALL_DIR" ]]; then
    echo "♻️  Removing previous installation..."
    rm -rf "$INSTALL_DIR"
fi

echo "📁 Creating environment in $INSTALL_DIR..."
python3 -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"

# ── 3. Install the package ──────────────────────────────────────
echo "⬇️  Installing laptop-guardian..."
pip install --upgrade pip -q
pip install git+https://github.com/stef41/laptop-guardian.git -q

echo "   Installed: $(pip show laptop-guardian | grep Version)"

# ── 4. Create launcher ──────────────────────────────────────────
LAUNCHER="$INSTALL_DIR/laptop-guardian"
cat > "$LAUNCHER" << 'EOF'
#!/bin/bash
source "$HOME/.laptop-guardian/venv/bin/activate"
exec laptop-guardian "$@"
EOF
chmod +x "$LAUNCHER"

# Add to PATH via symlink
if [[ -d "$HOME/.local/bin" ]] || mkdir -p "$HOME/.local/bin"; then
    ln -sf "$LAUNCHER" "$HOME/.local/bin/laptop-guardian"
fi

# ── 5. Platform-specific app integration ────────────────────────
if [[ "$(uname)" == "Darwin" ]]; then
    # macOS: create .app bundle
    APP_DIR="$HOME/Applications"
    APP_BUNDLE="$APP_DIR/Laptop Guardian.app"
    mkdir -p "$APP_DIR"
    rm -rf "$APP_BUNDLE"
    mkdir -p "$APP_BUNDLE/Contents/MacOS"
    mkdir -p "$APP_BUNDLE/Contents/Resources"

    cat > "$APP_BUNDLE/Contents/MacOS/Laptop Guardian" << 'APPLAUNCH'
#!/bin/bash
source "$HOME/.laptop-guardian/venv/bin/activate"
exec laptop-guardian
APPLAUNCH
    chmod +x "$APP_BUNDLE/Contents/MacOS/Laptop Guardian"

    cat > "$APP_BUNDLE/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Laptop Guardian</string>
    <key>CFBundleDisplayName</key>
    <string>Laptop Guardian</string>
    <key>CFBundleIdentifier</key>
    <string>com.laptopguardian.app</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleExecutable</key>
    <string>Laptop Guardian</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
PLIST
    cp /System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ToolbarAdvanced.icns \
       "$APP_BUNDLE/Contents/Resources/AppIcon.icns" 2>/dev/null || true
    echo "   Created: ~/Applications/Laptop Guardian.app"

elif [[ "$(uname)" == "Linux" ]]; then
    # Linux: create .desktop file
    DESKTOP_DIR="$HOME/.local/share/applications"
    mkdir -p "$DESKTOP_DIR"
    cat > "$DESKTOP_DIR/laptop-guardian.desktop" << EOF
[Desktop Entry]
Name=Laptop Guardian
Comment=Anti-theft laptop protection
Exec=$HOME/.laptop-guardian/venv/bin/laptop-guardian
Type=Application
Categories=Utility;Security;
StartupNotify=false
EOF
    echo "   Created: desktop entry (find it in your app launcher)"
fi

echo ""
echo "✅ Laptop Guardian installed!"
echo ""
echo "   How to launch:"
if [[ "$(uname)" == "Darwin" ]]; then
    echo "   • Open ~/Applications/Laptop Guardian (double-click)"
    echo "   • Or Spotlight: ⌘+Space → 'Laptop Guardian'"
elif [[ "$(uname)" == "Linux" ]]; then
    echo "   • Find 'Laptop Guardian' in your app launcher"
fi
echo "   • Or terminal: laptop-guardian"
echo ""
echo "   A shield icon will appear in your system tray."
echo "   Right-click it → set your phone name → click 'Arm Guardian'."
echo ""
