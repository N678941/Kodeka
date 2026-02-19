#!/usr/bin/env bash
set -e

echo "╔════════════════════════════════════════════╗"
echo "║          Installing Kodeka CLI 2026        ║"
echo "║   AI coding & general helper for terminal  ║"
echo "╚════════════════════════════════════════════╝"

if ! command -v python3 &> /dev/null; then
    echo "Python 3.10+ is required. Please install it first."
    exit 1
fi

INSTALL_DIR="$HOME/.kodeka"
mkdir -p "$INSTALL_DIR"

echo "Downloading latest version..."
# CHANGE THIS URL when you have real hosting / GitHub releases
curl -L -o "$INSTALL_DIR/kodeka.zip" "https://github.com/yourusername/kodeka/releases/latest/download/cli.zip" || {
    echo "Download failed. Check your internet or try manual install."
    exit 1
}

unzip -o "$INSTALL_DIR/kodeka.zip" -d "$INSTALL_DIR"
rm "$INSTALL_DIR/kodeka.zip"

chmod +x "$INSTALL_DIR/cli/kodeka.py"

# Create bin symlink
mkdir -p "$HOME/.local/bin"
ln -sf "$INSTALL_DIR/cli/kodeka.py" "$HOME/.local/bin/kodeka"

echo ""
echo "Kodeka installed! Run:"
echo "    kodeka"
echo ""
echo "First run will guide you through provider & key setup."
echo "Enjoy! 🚀"
