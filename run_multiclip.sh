#!/bin/bash

# Set up display environment
export DISPLAY=:0
export XAUTHORITY=/home/flintx/.Xauthority

# Change to the correct user if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Running as root, switching to user flintx..."
    su - flintx -c "cd /home/flintx/diff/project && source venv/bin/activate && python3 multiclip.py"
else
    # Running as regular user
    python3 multiclip.py
fi