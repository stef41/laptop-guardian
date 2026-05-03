#!/bin/bash
# Uninstall Laptop Guardian
set -e
echo "🗑️  Uninstalling Laptop Guardian..."
rm -rf "$HOME/.laptop-guardian"
rm -rf "$HOME/Applications/Laptop Guardian.app"
rm -rf "$HOME/.config/laptop-guardian"
echo "✅ Done. Laptop Guardian has been removed."
