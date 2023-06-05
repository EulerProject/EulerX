#!/bin/bash

# This script installs python2
sudo apt update
sudo apt install python2 --yes
sudo ln -s /usr/bin/python2 /usr/local/bin/python

# Download the dlv binary
# echo "Downloading new DLV binary"
wget https://www.dlvsystem.it/files/dlv.x86-64-linux-elf-static.bin

# Change permissions to make the binary executable
echo "Setting execute permissions for the DLV binary"
chmod +x /workspaces/EulerX/dlv.x86-64-linux-elf-static.bin

# Create a symbolic link to the binary
echo "Creating symbolic link for the DLV binary"
sudo ln -s /workspaces/EulerX/dlv.x86-64-linux-elf-static.bin /usr/local/bin/dlv

# Install clingo and graphviz using conda
echo "Installing clingo and graphviz"
sudo apt install graphviz --yes
sudo apt install gringo --yes

# Install pip
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
sudo python2 get-pip.py
sudo ln -s /usr/bin/pip2 /usr/local/bin/pip

# Install Python dependencies
echo "Installing Python dependencies"
pip install docopt==0.6.1
pip install pyyaml==5.3.1

# Change permissions to make y2d script executable
echo "Setting execute permissions for y2d script"
chmod +x /workspaces/EulerX/src-el/y2d

# Create a symbolic link to y2d script
echo "Creating symbolic link for y2d script"
sudo ln -s /workspaces/EulerX/src-el/y2d /usr/local/bin/y2d


# Change permissions to make euler2 script executable
echo "Setting execute permissions for euler2 script"
chmod +x /workspaces/EulerX/src-el/euler2

# Create a symbolic link to euler2 script
echo "Creating symbolic link for euler2 script"
sudo ln -s /workspaces/EulerX/src-el/euler2 /usr/local/bin/euler2


echo "Setup completed successfully"