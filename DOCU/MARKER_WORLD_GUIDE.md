# Marker World Guide

This guide explains the custom Gazebo world with ArUco marker poles and how to use it for robot perception testing.

## Overview

The marker world (`marker_world.world`) is a custom Gazebo environment designed for testing visual perception and localization. It features:

- **Ground Plane**: 20m × 20m flat surface with realistic friction
- **Four ArUco Marker Poles**: Positioned at square vertices forming a 6m × 6m square
- **Proper Lighting**: Sun (directional) + ambient lighting for camera visibility
- **Realistic Physics**: ODE physics engine with 1ms timestep

## Marker Pole Layout

The four marker poles are positioned to form a square centered at the origin:

```
        Y
        ^
        |
  pole53 (ID 53)          pole51 (ID 51)
    (-3, 3)                  (3, 3)
        ●─────────────────────●
        │                     │
        │                     │
        │      Robot (0,0)    │
        │          ●          │
        │                     │
        │                     │
        ●─────────────────────●
  pole54 (ID 54)          pole52 (ID 52)
    (-3, -3)                (3, -3)
        |
        └────────────────────────> X
```

**Marker Details:**
- **pole51** (ID 51): Position (3, 3, 0), facing inward at -135° (toward origin)
- **pole52** (ID 52): Position (3, -3, 0), facing inward at -45° (toward origin)
- **pole53** (ID 53): Position (-3, 3, 0), facing inward at 135° (toward origin)
- **pole54** (ID 54): Position (-3, -3, 0), facing inward at 45° (toward origin)

All markers are oriented to face the center of the square where the robot spawns.

## Robot Spawn Configuration

The robot spawns at the center of the marker square:

- **Position**: (0, 0, 0.1) - Center of square, slightly elevated
- **Orientation**: 0° yaw (facing +X axis, toward pole51 and pole52)
- **Camera View**: At least 2 markers (pole51 and pole52) should be visible in the initial camera view

## Installation

### 1. Marker Pole Models Location

The marker pole models are stored **locally in the workspace** for portability:

```bash
# Models are located at:
ros2_ws/src/my_robot_gazebo/models/pole51/
ros2_ws/src/my_robot_gazebo/models/pole52/
ros2_ws/src/my_robot_gazebo/models/pole53/
ros2_ws/src/my_robot_gazebo/models/pole54/
```

**Why local models?**
- ✅ Portable - works on any machine
- ✅ Version controlled with your project  
- ✅ No global system modifications
- ✅ Follows ROS 2 best practices

**If models are missing**, copy them from the provided assets:
```bash
cd ~/Desktop/ROARTASK
cp -r "ROAR26-SOLO-MISSION-SIMULATION-AND-TESTING-master/assests/Part 2 - ArUco Marker Poles/"* ros2_ws/src/my_robot_gazebo/models/
```

### 2. Verify Installation

Run the verification script to ensure everything is set up correctly:

```bash
cd ~/Desktop/ROARTASK
./verify_marker_world.sh
```

Expected output:
```
✓ All checks passed!
```

### 3. Build Workspace

Ensure the workspace is built with the latest changes:

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select my_robot_gazebo
source install/setup.bash
```

## Usage

### Launch Marker World

Start the simulation with the robot in the marker world:

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source install/setup.bash
ros2 launch my_robot_gazebo spawn_robot.launch.py
```

**What happens:**
1. Gazebo Ignition launches with `marker_world.world`
2. Robot spawns at origin (0, 0, 0.1)
3. Four marker poles appear at square vertices
4. Sensor bridges start (IMU, camera)
5. Robot state publisher starts for TF tree

### Verify Marker Visibility

Check that markers are visible in the camera view:

```bash
# Terminal 2: View camera feed
ros2 run rqt_image_view rqt_image_view
```

In the GUI:
1. Select topic: `/camera/image_raw`
2. You should see at least 2 marker poles in the camera view
3. Markers should be clearly visible with ArUco patterns

### Check Active Topics

Verify all expected topics are publishing:

```bash
# List all topics
ros2 topic list

# Expected topics:
# /camera/image_raw
# /camera/camera_info
# /imu/data
# /tf
# /tf_static
# /robot_description

# Check camera publishing rate
ros2 topic hz /camera/image_raw
# Expected: ~30 Hz

# Check IMU publishing rate
ros2 topic hz /imu/data
# Expected: ~1000 Hz (Gazebo simulation rate)
```

## World File Structure

The world file (`marker_world.world`) is organized as follows:

```xml
<world name="marker_world">
  <!-- Physics configuration -->
  <physics type="ode">
    <max_step_size>0.001</max_step_size>
    <real_time_factor>1</real_time_factor>
  </physics>
  
  <!-- Required Gazebo plugins -->
  <plugin name="gz::sim::systems::Physics"/>
  <plugin name="gz::sim::systems::UserCommands"/>
  <plugin name="gz::sim::systems::SceneBroadcaster"/>
  <plugin name="gz::sim::systems::Sensors"/>
  
  <!-- Lighting -->
  <light type="directional" name="sun"/>
  <ambient>0.4 0.4 0.4 1</ambient>
  
  <!-- Ground plane -->
  <model name="ground_plane">
    <!-- 20m x 20m plane with friction -->
  </model>
  
  <!-- Marker poles -->
  <include>
    <uri>model://pole51</uri>
    <pose>3 3 0 0 0 -2.356</pose>
  </include>
  <!-- ... pole52, pole53, pole54 ... -->
</world>
```

## Customization

### Adjust Marker Positions

To change marker positions, edit `marker_world.world`:

```xml
<!-- Example: Move pole51 further away -->
<include>
  <uri>model://pole51</uri>
  <pose>5 5 0 0 0 -2.356</pose>  <!-- Changed from (3, 3) to (5, 5) -->
</include>
```

After editing, rebuild the package:
```bash
cd ~/Desktop/ROARTASK/ros2_ws
colcon build --packages-select my_robot_gazebo
```

### Adjust Robot Spawn Position

To change where the robot spawns, edit `spawn_robot.launch.py`:

```python
spawn_robot = Node(
    package='ros_gz_sim',
    executable='create',
    arguments=[
        '-name', 'my_robot',
        '-topic', 'robot_description',
        '-x', '1.0',    # Changed from 0.0
        '-y', '0.0',
        '-z', '0.1',
        '-Y', '0.785'   # Changed from 0.0 (45° rotation)
    ]
)
```

### Add More Markers

To add additional marker poles:

1. Install the new pole model to `~/.gz/models/`
2. Add an `<include>` block in `marker_world.world`:
   ```xml
   <include>
     <uri>model://pole55</uri>
     <name>pole55</name>
     <pose>0 5 0 0 0 -1.571</pose>
   </include>
   ```
3. Rebuild the package

## Troubleshooting

### Markers Not Visible in Gazebo

**Problem**: Launch the world but marker poles don't appear.

**Solution**:
1. Check models are installed:
   ```bash
   ls ~/.gz/models/
   # Should show: pole51 pole52 pole53 pole54
   ```

2. Check Gazebo can find the models:
   ```bash
   gz model -l
   ```

3. Check for error messages in the terminal where you launched Gazebo

### Markers Not in Camera View

**Problem**: Markers appear in Gazebo but not in camera feed.

**Solution**:
1. Check robot orientation:
   ```bash
   gz topic -e -t /model/my_robot/pose
   ```

2. Verify camera is pointing forward (not down):
   - Camera should be pitched down 15° from horizontal
   - Check `camera_link` joint in URDF

3. Adjust lighting in world file if markers are too dark

### World File Not Found

**Problem**: Error message "Failed to load world file".

**Solution**:
1. Verify world file exists:
   ```bash
   ls ~/Desktop/ROARTASK/ros2_ws/src/my_robot_gazebo/worlds/marker_world.world
   ```

2. Rebuild the package:
   ```bash
   cd ~/Desktop/ROARTASK/ros2_ws
   colcon build --packages-select my_robot_gazebo
   source install/setup.bash
   ```

3. Check the launch file path is correct

## Next Steps

After successfully launching the marker world:

1. **Test ArUco Detection**: Integrate the ArUco tracking node to detect markers
2. **Visualize in RViz**: Add marker visualizations to RViz
3. **Record Data**: Use rosbag to record camera and IMU data
4. **Test Localization**: Use marker detections for robot localization

## References

- [Gazebo World Files](https://gazebosim.org/docs/latest/sdf_worlds)
- [ArUco Marker Detection](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html)
- [ROS 2 Gazebo Integration](https://github.com/gazebosim/ros_gz)

---

**Last Updated**: Task 9 completed - Marker world created and verified


## Step-by-Step Guide: Creating a Custom Gazebo World with Marker Poles

This section provides a complete walkthrough of how this marker world was created, so you can create your own custom worlds.

### Step 1: Understand the Project Structure

```
my_robot_gazebo/
├── worlds/              # World files (.world or .sdf)
├── models/              # Custom models (local to project)
│   ├── pole51/
│   ├── pole52/
│   ├── pole53/
│   └── pole54/
└── launch/              # Launch files
```

**Key principle**: Keep models local to your workspace for portability.

### Step 2: Copy Marker Pole Models to Workspace

```bash
cd ~/Desktop/ROARTASK

# Copy provided marker pole models to workspace
cp -r "ROAR26-SOLO-MISSION-SIMULATION-AND-TESTING-master/assests/Part 2 - ArUco Marker Poles/"* \
      ros2_ws/src/my_robot_gazebo/models/

# Verify models are copied
ls ros2_ws/src/my_robot_gazebo/models/
# Should show: pole51 pole52 pole53 pole54
```

**Why local models?**
- ✅ Portable across machines
- ✅ Version controlled with git
- ✅ No system-wide modifications needed

### Step 3: Create the World File

Create `marker_world.world` in `my_robot_gazebo/worlds/`:

```xml
<?xml version="1.0" ?>
<sdf version="1.9">
  <world name="marker_world">
    
    <!-- Step 3.1: Configure Physics -->
    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>
    
    <!-- Step 3.2: Add Required Gazebo Plugins -->
    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>
    
    <!-- Step 3.3: Add Lighting -->
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>
    
    <ambient>0.4 0.4 0.4 1</ambient>
    
    <!-- Step 3.4: Add Ground Plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>20 20</size>
            </plane>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>100</mu>
                <mu2>50</mu2>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>20 20</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
    
    <!-- Step 3.5: Include Marker Poles -->
    <include>
      <uri>model://pole51</uri>
      <name>pole51</name>
      <pose>3 3 0 0 0 -2.356</pose>
    </include>
    
    <include>
      <uri>model://pole52</uri>
      <name>pole52</name>
      <pose>3 -3 0 0 0 -0.785</pose>
    </include>
    
    <include>
      <uri>model://pole53</uri>
      <name>pole53</name>
      <pose>-3 3 0 0 0 2.356</pose>
    </include>
    
    <include>
      <uri>model://pole54</uri>
      <name>pole54</name>
      <pose>-3 -3 0 0 0 0.785</pose>
    </include>
    
  </world>
</sdf>
```

**Key points:**
- `<include>` uses `model://` URI to reference models
- `<pose>` format: `x y z roll pitch yaw`
- Yaw angles make poles face inward toward origin

### Step 4: Create Launch File with Local Model Path

Create `spawn_robot.launch.py` in `my_robot_gazebo/launch/`:

**CRITICAL STEP**: Set `GZ_SIM_RESOURCE_PATH` to use local models:

```python
#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Get package paths
    pkg_my_robot_description = get_package_share_directory('my_robot_description')
    pkg_my_robot_gazebo = get_package_share_directory('my_robot_gazebo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    
    # CRITICAL: Set model path to workspace models (local, not global)
    workspace_models_path = os.path.join(pkg_my_robot_gazebo, 'models')
    if 'GZ_SIM_RESOURCE_PATH' in os.environ:
        os.environ['GZ_SIM_RESOURCE_PATH'] = os.environ['GZ_SIM_RESOURCE_PATH'] + ':' + workspace_models_path
    else:
        os.environ['GZ_SIM_RESOURCE_PATH'] = workspace_models_path
    
    # Process robot URDF
    xacro_file = os.path.join(pkg_my_robot_description, 'urdf', 'my_robot.urdf.xacro')
    robot_description_content = Command(['xacro ', xacro_file])
    robot_description = ParameterValue(robot_description_content, value_type=str)
    
    # World file path
    world_file = os.path.join(pkg_my_robot_gazebo, 'worlds', 'marker_world.world')
    
    # Launch Gazebo with custom world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world_file]}.items()
    )
    
    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_description}]
    )
    
    # Spawn robot (delayed to ensure Gazebo is ready)
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'my_robot', '-topic', 'robot_description',
                   '-x', '0.0', '-y', '0.0', '-z', '0.1', '-Y', '0.0']
    )
    
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        gazebo,
        robot_state_publisher,
        TimerAction(period=3.0, actions=[spawn_robot])  # 3 second delay
    ])
```

**Critical steps:**
1. **Set `GZ_SIM_RESOURCE_PATH`** to workspace models directory (line 20-24)
2. **Use `ParameterValue`** wrapper for robot_description (line 29)
3. **Add `TimerAction`** to delay robot spawn by 3 seconds (line 54)

### Step 5: Update CMakeLists.txt

Ensure `CMakeLists.txt` installs the directories:

```cmake
install(DIRECTORY
  worlds
  models
  launch
  DESTINATION share/${PROJECT_NAME}
)
```

### Step 6: Build and Test

```bash
cd ~/Desktop/ROARTASK/ros2_ws

# Build the package
source /opt/ros/humble/setup.bash
colcon build --packages-select my_robot_gazebo

# Source workspace
source install/setup.bash

# Launch the world
ros2 launch my_robot_gazebo spawn_robot.launch.py
```

**Expected result:**
- Gazebo opens with marker world
- 4 poles visible at square vertices
- Robot spawns at center after 3 seconds
- At least 2 markers visible in camera view

### Step 7: Verify Setup

```bash
# Run verification script
cd ~/Desktop/ROARTASK
./verify_marker_world.sh

# Check topics are publishing
ros2 topic list | grep -E "(camera|imu)"

# View camera feed
ros2 run rqt_image_view rqt_image_view
# Select: /camera/image_raw
```

## Common Customizations

### Change Marker Positions

Edit `marker_world.world`:

```xml
<!-- Move pole51 to (5, 5) instead of (3, 3) -->
<include>
  <uri>model://pole51</uri>
  <pose>5 5 0 0 0 -2.356</pose>
</include>
```

### Change Robot Spawn Position

Edit `spawn_robot.launch.py`:

```python
spawn_robot = Node(
    arguments=[
        '-x', '2.0',    # Move 2m forward
        '-y', '1.0',    # Move 1m left
        '-z', '0.1',
        '-Y', '1.57'    # Rotate 90° (face +Y)
    ]
)
```

### Add More Marker Poles

1. Copy new pole model to `models/` directory
2. Add `<include>` block in world file:
   ```xml
   <include>
     <uri>model://pole55</uri>
     <name>pole55</name>
     <pose>0 5 0 0 0 -1.571</pose>
   </include>
   ```

## Summary of Implementation Steps

This is what was done to create the marker world:

1. ✅ **Copied marker pole models** from provided assets to `ros2_ws/src/my_robot_gazebo/models/`
2. ✅ **Created `marker_world.world`** with physics, lighting, ground plane, and 4 marker poles
3. ✅ **Created `spawn_robot.launch.py`** with:
   - `GZ_SIM_RESOURCE_PATH` set to local models directory
   - `ParameterValue` wrapper for robot_description
   - `TimerAction` to delay robot spawn by 3 seconds
4. ✅ **Updated `CMakeLists.txt`** to install worlds, models, and launch directories
5. ✅ **Built the package** with `colcon build`
6. ✅ **Created verification script** to check setup
7. ✅ **Documented everything** in this guide

## Key Lessons Learned

1. **Always use local models** (in workspace) instead of global (`~/.gz/models/`)
2. **Set `GZ_SIM_RESOURCE_PATH`** in launch file to point to local models
3. **Add delay to robot spawn** using `TimerAction` (Gazebo needs time to load)
4. **Use `ParameterValue` wrapper** for Command substitutions in ROS 2 launch files
5. **Test incrementally** - verify each step before moving to the next

---

**Created**: April 29, 2026 - Task 9 Implementation
