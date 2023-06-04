#!/bin/bash

# This script sets up a python 2.7 environment and installs necessary tools
echo "Creating a Python 2.7 environment named 'py2'"

# Create a Python 2.7 environment
conda create --name py2 python=2.7 --yes

# Activate the Python 2.7 environment
echo "Activating Python 2.7 environment"
source activate py2

# Unlink existing dlv binary
echo "Removing existing DLV binary"
sudo unlink /go/bin/dlv

# Download the dlv binary
# echo "Downloading new DLV binary"
# wget https://www.dlvsystem.it/files/dlv.x86-64-linux-elf-static.bin

# Change permissions to make the binary executable
echo "Setting execute permissions for the DLV binary"
chmod +x /workspaces/EulerX/dlv.x86-64-linux-elf-static.bin

# Create a symbolic link to the binary
echo "Creating symbolic link for the DLV binary"
sudo ln -s /workspaces/EulerX/dlv.x86-64-linux-elf-static.bin /usr/local/bin/dlv

# Install clingo and graphviz using conda
echo "Installing clingo and graphviz"
conda update -n base -c defaults conda --yes
conda install -c potassco clingo --yes
conda install -c conda-forge python-graphviz --yes

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