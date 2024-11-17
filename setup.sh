#!/usr/bin/env bash


# Create user's service directory
mkdir -p $HOME/.local/share/systemd/user

# Set file ownership
chown $USER: brightness.service

# Copy service to directory
echo "Creating systemd service"
cp brightness.service $HOME/.local/share/systemd/user/

# Reload daemon
echo "Reloading daemon"
systemctl --user daemon-reload

# Enable service
echo "Enabling service"
systemctl --user enable brightness.service

# Start service
echo "Starting service"
systemctl --user start brightness.service

echo "Done!"

# Check service
systemctl --user status brightness.service
