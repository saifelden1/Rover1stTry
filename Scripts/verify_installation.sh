#!/bin/bash

# ROS 2 + Gazebo Robot Simulation - Installation Verification Script
# This script verifies that all required dependencies are installed

set -e  # Exit on any error

echo "=========================================="
echo "ROS 2 + Gazebo Installation Verification"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

ERRORS=0

# Check OS version
echo "1. Checking OS version..."
if grep -q "22.04" /etc/os-release; then
    print_status "Ubuntu 22.04 detected"
else
    print_error "Ubuntu 22.04 not detected"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check ROS 2 Humble
echo "2. Checking ROS 2 Humble..."
if [ -d "/opt/ros/humble" ]; then
    print_status "ROS 2 Humble installed"
    source /opt/ros/humble/setup.bash
    
    # Try to get ROS 2 info
    if ros2 doctor --report 2>&1 | head -1 > /dev/null; then
        print_status "ROS 2 commands working"
    else
        print_warning "ROS 2 installed but commands may have issues"
    fi
else
    print_error "ROS 2 Humble not found"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check Gazebo Ignition
echo "3. Checking Gazebo Ignition..."
if command -v gz &> /dev/null; then
    VERSION=$(gz sim --version 2>&1 | head -1)
    print_status "Gazebo Ignition installed: $VERSION"
elif command -v ign &> /dev/null; then
    VERSION=$(ign gazebo --version 2>&1 | head -1)
    print_status "Gazebo Ignition installed: $VERSION"
else
    print_error "Gazebo Ignition not found"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check required ROS 2 packages
echo "4. Checking required ROS 2 packages..."

# For Gazebo Ignition, we use ros-gz packages instead of gazebo-ros-pkgs
REQUIRED_PACKAGES=(
    "ros-humble-ros-gz"
    "ros-humble-ros-gz-sim"
    "ros-humble-robot-state-publisher"
    "ros-humble-joint-state-publisher"
    "ros-humble-xacro"
    "ros-humble-rviz2"
)

for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if dpkg -l | grep -q "^ii  $pkg "; then
        print_status "$pkg"
    else
        print_error "$pkg - NOT INSTALLED"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# Check development tools
echo "5. Checking development tools..."

DEV_TOOLS=(
    "python3-colcon-common-extensions"
    "python3-rosdep"
)

for tool in "${DEV_TOOLS[@]}"; do
    if dpkg -l | grep -q "^ii  $tool "; then
        print_status "$tool"
    else
        print_error "$tool - NOT INSTALLED"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# Check additional useful packages
echo "6. Checking additional useful packages..."

OPTIONAL_PACKAGES=(
    "ros-humble-rqt"
    "ros-humble-rqt-graph"
    "ros-humble-tf2-tools"
)

for pkg in "${OPTIONAL_PACKAGES[@]}"; do
    if dpkg -l | grep -q "^ii  $pkg "; then
        print_status "$pkg"
    else
        print_warning "$pkg - NOT INSTALLED (optional but recommended)"
    fi
done
echo ""

# Final summary
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All required packages are installed!${NC}"
    echo "=========================================="
    echo ""
    echo "Your system is ready for ROS 2 + Gazebo development."
    echo ""
    echo "Next steps:"
    echo "1. Source ROS 2: source /opt/ros/humble/setup.bash"
    echo "2. Create workspace: mkdir -p ~/ros2_ws/src && cd ~/ros2_ws"
    echo "3. Build packages: colcon build"
    echo "4. Source workspace: source install/setup.bash"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Installation incomplete: $ERRORS error(s) found${NC}"
    echo "=========================================="
    echo ""
    echo "Please install missing packages before proceeding."
    exit 1
fi
