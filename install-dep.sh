#!/bin/bash

echo "[*] Installing Python dependencies..."
pip install -r requirements.txt

echo "[*] Installing system dependencies (Ghostscript)..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update && sudo apt install -y ghostscript
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ghostscript
else
    echo "[!] Please install Ghostscript manually for your OS."
fi

echo "[*] Setup complete."