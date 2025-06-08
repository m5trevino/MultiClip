#!/bin/bash

echo "Setting up MultiClip System..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
chmod +x multiclip.py
chmod +x snippers-view.py
chmod +x snippers-save.py
chmod +x ordely.py

# Create desktop entry (optional)
echo "Creating desktop entry..."
cat << 'DESKTOP_EOF' > ~/.local/share/applications/multiclip.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=MultiClip System
Comment=Advanced Clipboard Manager with Orderly and Snippers
Exec=$(pwd)/venv/bin/python $(pwd)/multiclip.py
Icon=accessories-clipboard
Terminal=false
Categories=Utility;
DESKTOP_EOF

echo "Setup complete!"
echo ""
echo "To run the system:"
echo "  ./venv/bin/python multiclip.py"
echo ""
echo "Or create an alias in your ~/.bashrc:"
echo "  alias multiclip='$(pwd)/venv/bin/python $(pwd)/multiclip.py'"
