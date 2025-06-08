#!/bin/bash

# Set up environment for root to access your user's X session
export DISPLAY=:0
export XAUTHORITY=/home/flintx/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000
export HOME=/home/flintx

# Set up pyenv environment
export PYENV_ROOT=/home/flintx/.pyenv
export PATH="$PYENV_ROOT/bin:$PATH"

# Change to working directory
cd /home/flintx/multiclip

# Activate the virtual environment and run
source /home/flintx/.pyenv/versions/multiclip/bin/activate
exec python multiclip.py
