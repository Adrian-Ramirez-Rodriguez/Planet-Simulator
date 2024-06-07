#!/bin/bash

# Check if Python is already installed
if ! command -v python3 &>/dev/null; then
    # If Python is not installed, download and install Python
    echo "Installing Python..."
    if [[ $(uname -s) == "Linux" ]]; then
        # For Linux
        curl -O https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz
        tar -xf Python-3.9.7.tgz
        cd Python-3.9.7
        ./configure
        make
        sudo make install
        cd ..
        rm -rf Python-3.9.7*
    elif [[ $(uname -s) == "Darwin" ]]; then
        # For macOS
        curl -O https://www.python.org/ftp/python/3.9.7/python-3.9.7-macosx10.9.pkg
        sudo installer -pkg python-3.9.7-macosx10.9.pkg -target /
        rm python-3.9.7-macosx10.9.pkg
    fi
else
    echo "Python is already installed."
fi

# Install Pygame
echo "Installing Pygame..."
pip3 install pygame

echo "Installation completed."