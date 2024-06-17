#!/bin/sh
# This script updates the package list and installs the specified packages

# Update package list
apt-get update

# Install necessary packages without recommended packages
apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libxext-dev \
    libxrender-dev \
    libxtst-dev

# Clean up
rm -rf /var/lib/apt/lists/*

gunicorn --bind=0.0.0.0 --timeout 1800 application:application
