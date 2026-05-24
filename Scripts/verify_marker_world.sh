#!/bin/bash
# Verification script for marker world setup
# This script checks that all marker pole models are installed correctly

echo "=========================================="
echo "Marker World Verification Script"
echo "=========================================="
echo ""

# Check if marker models directory exists in workspace
echo "1. Checking workspace models directory..."
MODELS_DIR="$HOME/Desktop/ROARTASK/ros2_ws/src/my_robot_gazebo/models"
if [ -d "$MODELS_DIR" ]; then
    echo "   ✓ Models directory exists: $MODELS_DIR"
else
    echo "   ✗ Models directory not found: $MODELS_DIR"
    exit 1
fi
echo ""

# Check for each marker pole model
echo "2. Checking marker pole models..."
MODELS=("pole51" "pole52" "pole53" "pole54")
ALL_PRESENT=true

for model in "${MODELS[@]}"; do
    if [ -d "$MODELS_DIR/$model" ]; then
        echo "   ✓ $model found"
        
        # Check for required files
        if [ -f "$MODELS_DIR/$model/model.config" ] && [ -f "$MODELS_DIR/$model/model.sdf" ]; then
            echo "      ✓ model.config and model.sdf present"
        else
            echo "      ✗ Missing model.config or model.sdf"
            ALL_PRESENT=false
        fi
    else
        echo "   ✗ $model not found"
        ALL_PRESENT=false
    fi
done
echo ""

# Check if world file exists
echo "3. Checking world file..."
WORLD_FILE="$HOME/Desktop/ROARTASK/ros2_ws/src/my_robot_gazebo/worlds/marker_world.world"
if [ -f "$WORLD_FILE" ]; then
    echo "   ✓ marker_world.world found"
else
    echo "   ✗ marker_world.world not found at: $WORLD_FILE"
    exit 1
fi
echo ""

# Check if launch file exists
echo "4. Checking launch file..."
LAUNCH_FILE="$HOME/Desktop/ROARTASK/ros2_ws/src/my_robot_gazebo/launch/spawn_robot.launch.py"
if [ -f "$LAUNCH_FILE" ]; then
    echo "   ✓ spawn_robot.launch.py found"
else
    echo "   ✗ spawn_robot.launch.py not found at: $LAUNCH_FILE"
    exit 1
fi
echo ""

# Check if workspace is built
echo "5. Checking workspace build..."
if [ -d "$HOME/Desktop/ROARTASK/ros2_ws/install/my_robot_gazebo" ]; then
    echo "   ✓ my_robot_gazebo package built"
else
    echo "   ✗ my_robot_gazebo package not built"
    echo "   Run: cd ~/Desktop/ROARTASK/ros2_ws && colcon build"
    exit 1
fi
echo ""

# Final summary
echo "=========================================="
if [ "$ALL_PRESENT" = true ]; then
    echo "✓ All checks passed!"
    echo ""
    echo "To launch the marker world:"
    echo "  cd ~/Desktop/ROARTASK/ros2_ws"
    echo "  source install/setup.bash"
    echo "  ros2 launch my_robot_gazebo spawn_robot.launch.py"
else
    echo "✗ Some checks failed. Please fix the issues above."
    echo ""
    echo "To install marker models in workspace:"
    echo "  cd ~/Desktop/ROARTASK"
    echo "  cp -r 'ROAR26-SOLO-MISSION-SIMULATION-AND-TESTING-master/assests/Part 2 - ArUco Marker Poles/'* ros2_ws/src/my_robot_gazebo/models/"
fi
echo "=========================================="
