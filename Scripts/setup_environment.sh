#!/bin/bash

# ROS 2 + Gazebo Robot Simulation - Environment Setup Script
# This script installs all required dependencies for the ROAR'26 Solo Mission Part 2 assignment
# Target: Ubuntu 22.04 with ROS 2 Humble

set -e  # Exit on any error

echo "=========================================="
echo "ROS 2 + Gazebo Environment Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on Ubuntu 22.04
print_status "Checking OS version..."
if ! grep -q "22.04" /etc/os-release; then
    print_error "This script requires Ubuntu 22.04"
    exit 1
fi
print_status "Ubuntu 22.04 detected ✓"

# Check if ROS 2 Humble is installed
print_status "Checking ROS 2 Humble installation..."
if [ ! -d "/opt/ros/humble" ]; then
    print_error "ROS 2 Humble is not installed. Please install it first."
    print_error "Visit: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html"
    exit 1
fi
print_status "ROS 2 Humble found ✓"

# Source ROS 2 environment
print_status "Sourcing ROS 2 environment..."
source /opt/ros/humble/setup.bash

# Update package lists
print_status "Updating package lists..."
sudo apt-get update

# Install required ROS 2 packages
print_status "Installing ROS 2 packages..."

# Install gazebo-ros-pkgs
if ! dpkg -l | grep -q "ros-humble-gazebo-ros-pkgs"; then
    print_status "Installing ros-humble-gazebo-ros-pkgs..."
    sudo apt-get install -y ros-humble-gazebo-ros-pkgs
else
    print_status "ros-humble-gazebo-ros-pkgs already installed ✓"
fi

# Install robot-state-publisher
if ! dpkg -l | grep -q "ros-humble-robot-state-publisher"; then
    print_status "Installing ros-humble-robot-state-publisher..."
    sudo apt-get install -y ros-humble-robot-state-publisher
else
    print_status "ros-humble-robot-state-publisher already installed ✓"
fi

# Install joint-state-publisher
if ! dpkg -l | grep -q "ros-humble-joint-state-publisher"; then
    print_status "Installing ros-humble-joint-state-publisher..."
    sudo apt-get install -y ros-humble-joint-state-publisher
else
    print_status "ros-humble-joint-state-publisher already installed ✓"
fi

# Install development tools
print_status "Installing development tools..."

# Install colcon
if ! dpkg -l | grep -q "python3-colcon-common-extensions"; then
    print_status "Installing python3-colcon-common-extensions..."
    sudo apt-get install -y python3-colcon-common-extensions
else
    print_status "python3-colcon-common-extensions already installed ✓"
fi

# Install rosdep
if ! dpkg -l | grep -q "python3-rosdep"; then
    print_status "Installing python3-rosdep..."
    sudo apt-get install -y python3-rosdep
else
    print_status "python3-rosdep already installed ✓"
fi

# Initialize rosdep if not already done
if [ ! -f "/etc/ros/rosdep/sources.list.d/20-default.list" ]; then
    print_status "Initializing rosdep..."
    sudo rosdep init
fi

print_status "Updating rosdep..."
rosdep update

# Install additional useful packages
print_status "Installing additional useful packages..."
sudo apt-get install -y \
    ros-humble-xacro \
    ros-humble-rviz2 \
    ros-humble-rqt \
    ros-humble-rqt-graph \
    ros-humble-tf2-tools \
    ros-humble-urdf-tutorial

echo ""
echo "=========================================="
echo "Verification"
echo "=========================================="
echo ""

# Verify installations
print_status "Verifying installations..."

# Check ROS 2 version
print_status "ROS 2 version:"
ros2 doctor --report 2>&1 | head -1 || echo "  (ros2 command available)"

# Check Gazebo version
print_status "Gazebo version:"
if command -v ign &> /dev/null; then
    ign gazebo --version
elif command -v gz &> /dev/null; then
    gz sim --version
else
    print_error "Gazebo Ignition not found!"
    print_error "Please install Gazebo Fortress or later"
    exit 1
fi

# Verify required packages
print_status "Verifying required ROS 2 packages..."
MISSING_PACKAGES=0

for pkg in "ros-humble-gazebo-ros-pkgs" "ros-humble-robot-state-publisher" "ros-humble-joint-state-publisher"; do
    if dpkg -l | grep -q "$pkg"; then
        echo "  ✓ $pkg"
    else
        print_error "  ✗ $pkg - NOT INSTALLED"
        MISSING_PACKAGES=$((MISSING_PACKAGES + 1))
    fi
done

for tool in "python3-colcon-common-extensions" "python3-rosdep"; do
    if dpkg -l | grep -q "$tool"; then
        echo "  ✓ $tool"
    else
        print_error "  ✗ $tool - NOT INSTALLED"
        MISSING_PACKAGES=$((MISSING_PACKAGES + 1))
    fi
done

echo ""
if [ $MISSING_PACKAGES -eq 0 ]; then
    echo -e "${GREEN}=========================================="
    echo "✓ All packages installed successfully!"
    echo "==========================================${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Source ROS 2 in your terminal: source /opt/ros/humble/setup.bash"
    echo "2. Add to ~/.bashrc for automatic sourcing: echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc"
    echo "3. Create your ROS 2 workspace: mkdir -p ~/ros2_ws/src"
    echo "4. Start building your robot!"
else
    print_error "=========================================="
    print_error "Installation incomplete: $MISSING_PACKAGES package(s) missing"
    print_error "=========================================="
    exit 1
fi
