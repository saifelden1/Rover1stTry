# Robot Perception Package

Perception integration package for ArUco marker detection and tracking on the Mars rover robot.

## What This Package Does

Integrates the ArUco marker detection node with the robot's camera sensor, providing marker detection, pose estimation, and TF frame publishing for visual localization.

## Status

🚧 **In Development** - This package is currently being set up for Task 10.

The ArUco detection launch file will be created here to:
- Launch the aruco_tracking node
- Configure marker detection parameters
- Remap camera topics to match the detection node's expectations
- Publish detected marker poses to TF tree

## Planned Features

### ArUco Marker Detection
- Detect ArUco markers from dictionary DICT_7X7_1000 (IDs 51-54)
- Marker size: 0.15m × 0.15m
- Real-time pose estimation
- TF frame publishing for each detected marker

### Topics

**Subscribed**:
- `/camera/image_raw` - RGB camera feed from robot
- `/camera/camera_info` - Camera calibration data

**Published**:
- `/aruco_markers` - Visualization markers for RViz
- `/perception/detected_aruco` - Detected marker information
- `/tf` - Transform frames for detected markers

## Dependencies

- `sensor_msgs`: Camera image and info messages
- `tf2_ros`: Transform broadcasting
- `vision_msgs`: Detection result messages
- `visualization_msgs`: Marker visualization
- `aruco_tracking`: ArUco detection node (external package)

## Usage

Once implemented, launch ArUco detection with:

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source install/setup.bash
ros2 launch my_robot_perception aruco_detection.launch.py
```

This should be run alongside the main simulation:

```bash
# Terminal 1: Launch simulation
ros2 launch my_robot_gazebo spawn_robot.launch.py

# Terminal 2: Launch ArUco detection
ros2 launch my_robot_perception aruco_detection.launch.py
```

## Verification

### Check Detection Node is Running

```bash
ros2 node list | grep aruco
# Should show: /aruco_node
```

### Check Detection Topics

```bash
ros2 topic list | grep aruco
# Should show: /aruco_markers, /perception/detected_aruco
```

### View Detected Markers

```bash
ros2 topic echo /aruco_markers
# Should show marker visualization data when markers are visible
```

### Check TF Frames

```bash
ros2 run tf2_ros tf2_echo camera_link marker_51
# Should show transform when marker 51 is detected
```

## Configuration

### Marker Parameters

The ArUco detection node will be configured with:
- **Dictionary Type**: DICT_7X7_1000 (arucoDictType=7)
- **Marker Size**: 0.15m (markerSize=0.15)
- **Detection Rate**: 30 Hz (matches camera rate)

### Topic Remapping

The launch file will remap topics to match the aruco_tracking node's expectations:
- `/camera/image_raw` → `/image_raw`
- `/camera/camera_info` → `/camera/color/camera_info`

## Related Packages

- **[aruco_tracking](../aruco_tracking/)**: External ArUco detection node
- **[my_robot_description](../my_robot_description/)**: Robot model with camera sensor
- **[my_robot_gazebo](../my_robot_gazebo/)**: Simulation environment with marker poles

## Package Structure

```
my_robot_perception/
├── launch/
│   └── aruco_detection.launch.py  # (To be created in Task 10)
├── CMakeLists.txt
├── package.xml
└── README.md                       # This file
```

## Next Steps

Task 10 will implement:
1. Create `aruco_detection.launch.py` launch file
2. Configure aruco_tracking node with proper parameters
3. Set up topic remapping for camera feeds
4. Verify marker detection in simulation
5. Test TF frame publishing for detected markers
