#!/bin/bash
# Clear Gazebo cache to ensure fresh world loads

echo "Clearing Gazebo cache..."
rm -rf ~/.gz/sim/*/server.lock
rm -rf ~/.gz/sim/*/default.log
echo "✓ Gazebo cache cleared"
