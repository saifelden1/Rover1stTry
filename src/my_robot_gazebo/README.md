# Robot Gazebo Package

Custom Gazebo simulation environment for the 6-wheeled Mars rover with ArUco marker poles.

## What This Package Does

Provides the simulation world and launch files for spawning the robot in a custom Gazebo environment with four ArUco marker poles positioned in a square formation.

## Quick Start

### Launch Simulation

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source install/setup.bash
ros2 launch my_robot_gazebo spawn_robot.launch.py
```

This launches:
- Gazebo Ignition (Harmonic) with marker_world.world
- Robot spawned at origin (0, 0, 0.1)
- Robot state publisher with use_sim_time=true
- Sensor bridges (IMU, camera, odometry)
- Differential drive control bridge

## Files

### Launch Files
- **`spawn_robot.launch.py`**: Main launch file that starts Gazebo with the marker world and spawns the robot with all sensor bridges

### World Files
- **`marker_world.world`**: Custom Gazebo world with ground plane, lighting, and 4 ArUco marker poles

### Models
- **`pole51/`**: ArUco marker pole with ID 51 (positioned at 3, 3, 0)
- **`pole52/`**: ArUco marker pole with ID 52 (positioned at 3, -3, 0)
- **`pole53/`**: ArUco marker pole with ID 53 (positioned at -3, 3, 0)
- **`pole54/`**: ArUco marker pole with ID 54 (positioned at -3, -3, 0)

## World Configuration

### Marker Pole Positions

The four poles form a 6m × 6m square centered at the origin:

```
     Y
     ^
     |
  3  +  pole53 (ID 53)        pole51 (ID 51)
     |
  0  +-----------> X  (Robot spawns here)
     |
 -3  +  pole54 (ID 54)        pole52 (ID 52)
     |
    -3          0              3
```

All markers face inward toward the origin for optimal detection.

### Physics Configuration

- **Engine**: ODE (Open Dynamics Engine)
- **Max step size**: 0.001s (1ms)
- **Real-time factor**: 1.0 (real-time simulation)
- **Update rate**: 1000 Hz

### Lighting

- **Sun**: Directional light from above (simulates outdoor lighting)
- **Ambient**: 0.4, 0.4, 0.4 (soft fill light)

## Dependencies

- `gazebo_ros`: ROS 2 integration for Gazebo
- `gazebo_plugins`: Standard Gazebo plugins
- `ros_gz_sim`: Gazebo Ignition bridge
- `ros_gz_bridge`: Topic/service bridging

## Sensor Bridges

The launch file automatically creates bridges for:

- **IMU**: `/imu/data` (sensor_msgs/Imu)
- **Camera Image**: `/camera/image_raw` (sensor_msgs/Image)
- **Camera Info**: `/camera/camera_info` (sensor_msgs/CameraInfo)
- **Odometry**: `/odom` (nav_msgs/Odometry)
- **Command Velocity**: `/cmd_vel` (geometry_msgs/Twist)

## Verification

### Check Gazebo is Running

```bash
gz topic -l
# Should show Gazebo topics
```

### Check Robot Spawned

```bash
gz model -l
# Should show: my_robot
```

### Check Sensor Topics

```bash
ros2 topic list
# Should show: /imu/data, /camera/image_raw, /camera/camera_info, /odom, /cmd_vel
```

### View Camera Feed

```bash
ros2 run rqt_image_view rqt_image_view
# Select topic: /camera/image_raw
```

## Troubleshooting

### Robot Not Spawning

**Problem**: Robot doesn't appear in Gazebo
**Solution**: The launch file includes a 3-second delay to allow Gazebo to fully load. If the robot still doesn't spawn, try:

```bash
# Check if Gazebo is ready
gz topic -l

# Manually spawn robot
ros2 run ros_gz_sim create -topic robot_description -name my_robot -x 0 -y 0 -z 0.1
```

### Markers Not Visible

**Problem**: ArUco marker poles don't appear in world
**Solution**: Verify models are in the package:

```bash
ls src/my_robot_gazebo/models/
# Should show: pole51 pole52 pole53 pole54
```

Also check that models are in `~/.gz/models/`:

```bash
ls ~/.gz/models/
# Should include: pole51 pole52 pole53 pole54
```

### Sensor Topics Not Publishing

**Problem**: `/imu/data` or `/camera/image_raw` topics don't exist
**Solution**: Check that bridges are running:

```bash
ros2 node list | grep bridge
# Should show bridge nodes

# Check bridge configuration
ros2 topic info /imu/data
ros2 topic info /camera/image_raw
```

### Gazebo Crashes or Freezes

**Problem**: Gazebo becomes unresponsive
**Solution**: 
1. Check system resources (Gazebo requires significant CPU/GPU)
2. Reduce physics update rate in world file
3. Close other applications to free resources

## Configuration

### Spawn Position

To change robot spawn position, edit `spawn_robot.launch.py`:

```python
spawn_entity = Node(
    package='ros_gz_sim',
    executable='create',
    arguments=[
        '-topic', 'robot_description',
        '-name', 'my_robot',
        '-x', '0.0',  # Change X position
        '-y', '0.0',  # Change Y position
        '-z', '0.1'   # Change Z position (height)
    ],
    output='screen'
)
```

### World Modifications

To modify the world (add objects, change lighting, etc.), edit `worlds/marker_world.world`.

## Related Documentation

- **[MARKER_WORLD_GUIDE.md](../../../MARKER_WORLD_GUIDE.md)**: Detailed guide on world creation
- **[Main README](../../../README.md)**: Project overview and quick start
- **[Robot Description README](../my_robot_description/README.md)**: Robot model documentation

## Package Structure

```
my_robot_gazebo/
├── launch/
│   └── spawn_robot.launch.py    # Main simulation launch file
├── worlds/
│   └── marker_world.world        # Custom Gazebo world
├── models/
│   ├── pole51/                   # ArUco marker pole models
│   ├── pole52/
│   ├── pole53/
│   └── pole54/
├── CMakeLists.txt
├── package.xml
└── README.md                     # This file
```
