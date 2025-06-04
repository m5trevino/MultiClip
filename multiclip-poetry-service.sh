#!/bin/bash

# Set up environment for root to access user's X session
export DISPLAY=:0
export XAUTHORITY=/home/flintx/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000
export HOME=/home/flintx

# Change to working directory
cd /home/flintx/multiclip

# Use root's poetry to run (since we need root for hotkeys anyway)
poetry run python multiclip.py
