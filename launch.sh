#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Virtual environment not found. Running setup..."
    cd "$SCRIPT_DIR"
    ./setup.sh
fi

# Activate virtual environment and run
cd "$SCRIPT_DIR"
source venv/bin/activate
python multiclip.py "$@"
