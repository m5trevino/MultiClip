#!/bin/bash

echo "Setting up MultiClip System..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
chmod +x run_multiclip.sh
chmod +x multiclip.py

# Create desktop entry (optional)
echo "Creating desktop entry..."
mkdir -p ~/.local/share/applications
cat << DESKTOP_EOF > ~/.local/share/applications/multiclip.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=MultiClip System
Comment=Advanced Clipboard Manager with Orderly and Snippers
Exec=$SCRIPT_DIR/run_multiclip.sh
Icon=accessories-clipboard
Terminal=false
Categories=Utility;
DESKTOP_EOF

echo "Setup complete!"
echo ""
echo "To run the system:"
echo "  ./run_multiclip.sh"
echo ""
echo "Or run setup first if you haven't:"
echo "  ./setup.sh"