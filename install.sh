#!/bin/bash
# Laptop Guardian — one-command installer for macOS
# Usage: curl -sL https://raw.githubusercontent.com/stef41/laptop-guardian/main/install.sh | bash
set -e

APP_NAME="Laptop Guardian"
INSTALL_DIR="$HOME/.laptop-guardian"
APP_DIR="$HOME/Applications"
APP_BUNDLE="$APP_DIR/Laptop Guardian.app"

echo ""
echo "🛡️  Installing Laptop Guardian..."
echo ""

# ── 1. Ensure Homebrew is available ──────────────────────────────
if ! command -v brew &>/dev/null; then
    echo "📦 Installing Homebrew (macOS package manager)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add brew to PATH for Apple Silicon
    if [[ -f /opt/homebrew/bin/brew ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi

# ── 2. Ensure Python 3 is available ─────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "🐍 Installing Python 3..."
    brew install python
fi

echo "   Python: $(python3 --version)"

# ── 3. Create isolated virtual environment ──────────────────────
if [[ -d "$INSTALL_DIR" ]]; then
    echo "♻️  Removing previous installation..."
    rm -rf "$INSTALL_DIR"
fi

echo "📁 Creating environment in $INSTALL_DIR..."
python3 -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"

# ── 4. Install the package ──────────────────────────────────────
echo "⬇️  Installing laptop-guardian..."
pip install --upgrade pip -q
pip install git+https://github.com/stef41/laptop-guardian.git -q

echo "   Installed: $(pip show laptop-guardian | grep Version)"

# ── 5. Create a double-clickable .app bundle ────────────────────
echo "🖥️  Creating app in $APP_DIR..."
mkdir -p "$APP_DIR"
rm -rf "$APP_BUNDLE"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Launcher script
cat > "$APP_BUNDLE/Contents/MacOS/Laptop Guardian" << 'LAUNCHER'
#!/bin/bash
DIR="$(dirname "$(dirname "$(dirname "$(realpath "$0")")")")"
source "$HOME/.laptop-guardian/venv/bin/activate"
exec laptop-guardian
LAUNCHER
chmod +x "$APP_BUNDLE/Contents/MacOS/Laptop Guardian"

# Info.plist
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

# App icon (use a system icon as placeholder)
cp /System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ToolbarAdvanced.icns \
   "$APP_BUNDLE/Contents/Resources/AppIcon.icns" 2>/dev/null || true

echo ""
echo "✅ Laptop Guardian installed!"
echo ""
echo "   How to launch:"
echo "   • Open '~/Applications/Laptop Guardian' (double-click)"
echo "   • Or Spotlight: press ⌘+Space, type 'Laptop Guardian'"
echo "   • Or terminal: laptop-guardian"
echo ""
echo "   A 🛡️ icon will appear in your menu bar."
echo "   Click it → set your phone name → click 'Arm Guardian'."
echo ""
