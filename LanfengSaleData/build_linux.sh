#!/bin/bash

# Linux Build Script for FMS Enterprise
# Requires: python3, pip, pyinstaller

# 1. Install Requirements
# pip install pyinstaller mysql-connector-python sshtunnel PyQt5

# 2. Build Encrypted Executable
echo "Building FMS Enterprise for Linux..."

pyinstaller --noconfirm --onefile --windowed \
    --icon "icon.png" \
    --name "FMS_Enterprise_v2" \
    --add-data "icon.png:." \
    --add-data "logo.png:." \
    --hidden-import "mysql.connector.plugins" \
    "LanfengSaleAnalysis.py"

echo "Build Complete. Check 'dist/' folder."
