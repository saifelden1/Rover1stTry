# ROS 2 Workspace Aliases Guide

Quick reference for all available ROS 2 workspace aliases.

## Available Aliases

### `rosb` - Build Workspace
**Command:** `rosb`
**What it does:**
- Changes to workspace directory
- Sources ROS 2 Humble
- Builds all packages with colcon
- Sources the workspace
- Displays success message

**Use when:** You've made changes to code and need to rebuild

---

### `rosgp` - Launch Gazebo Simulation (Main)
**Command:** `rosgp`
**What it does:**
- Kills any existing Gazebo processes
- Changes to workspace directory
- Sources the workspace
- Launches Gazebo with **marker world** (ArUco poles)
- Spawns robot at origin
- Starts all sensor bridges (camera, IMU, odom)
- Starts robot_state_publisher

**Use when:** Starting the main simulation with ArUco marker poles

**World:** `marker_world.world` with 4 ArUco marker poles at:
- pole51: (3, 3, 0)
- pole52: (3, -3, 0)
- pole53: (-3, 3, 0)
- pole54: (-3, -3, 0)

---

### `rosd` - Launch RViz Visualization
**Command:** `rosd`
**What it does:**
- Changes to workspace directory
- Sources the workspace
- Launches RViz2 for visualization

**Use when:** You want to visualize the robot alongside Gazebo

**Typical workflow:**
```bash
# Terminal 1: Launch simulation
rosgp

# Terminal 2: Launch RViz (wait for Gazebo to load first)
rosd
```

**Note:** Does NOT launch robot_state_publisher (expects it to be running from `rosgp`)

---

### `rosgu` - Launch Teleop GUI
**Command:** `rosgu`
**What it does:**
- Changes to workspace directory
- Sources the workspace
- Launches robot teleop GUI for manual control

**Use when:** You want to manually control the robot with a GUI

**Publishes to:** `/cmd_vel` topic

---

### `rosg` - Launch Gazebo with Test World (Legacy)
**Command:** `rosg`
**What it does:**
- Kills any existing Gazebo processes
- Changes to workspace directory
- Sources the workspace
- Launches Gazebo with **empty world + colored balls**

**Use when:** Testing basic robot functionality without ArUco markers

**World:** `empty_with_sensors.sdf` with colored spheres for visual testing

---

### `rosar` - Launch ArUco Detection
**Command:** `rosar`
**What it does:**
- Changes to workspace directory
- Sources the workspace
- Launches ArUco marker detection node
- Subscribes to `/camera/image_raw` and `/camera/camera_info`
- Publishes detected markers to `/aruco_markers` and `/perception/detected_aruco`
- Publishes TF frames for detected markers

**Use when:** You want to detect ArUco markers in the simulation

**Typical workflow:**
```bash
# Terminal 1: Launch simulation
rosgp

# Terminal 2: Launch ArUco detection
rosar

# Terminal 3: (Optional) Launch RViz to visualize
rosd
```

**Parameters:**
- Dictionary: DICT_7X7_1000 (type 7)
- Marker size: 0.15m (15cm)
- Detects markers: 51, 52, 53, 54

---

## Typical Workflows

### Full Simulation with ArUco Detection
```bash
# Terminal 1: Launch Gazebo simulation
rosgp

# Terminal 2: Launch ArUco detection (wait for Gazebo to load)
rosar

# Terminal 3: Launch RViz for visualization
rosd

# Terminal 4: (Optional) Launch teleop for manual control
rosgu
```

### Full Simulation with Visualization
```bash
# Terminal 1: Launch Gazebo simulation
rosgp

# Terminal 2: Launch RViz (wait 3-5 seconds for Gazebo to load)
rosd

# Terminal 3: (Optional) Launch teleop for manual control
rosgu
```

### Build and Test
```bash
# Build workspace
rosb

# Launch simulation
rosgp
```

### Quick Rebuild
```bash
# If simulation is running, kill it first
pkill -9 ruby

# Rebuild
rosb

# Relaunch
rosgp
```

---

## Troubleshooting

### "Duplicate robot_state_publisher" Error
**Symptom:** Warning about nodes with exact same name
**Cause:** Running both `rosg` and `rosgp` together, or old processes not killed
**Fix:** 
```bash
pkill -9 ruby
pkill -9 rviz2
# Then relaunch
```

### "Frame not found" in RViz
**Symptom:** RViz shows "No transform from [frame] to [frame]"
**Cause:** robot_state_publisher not running or Gazebo not fully loaded
**Fix:**
1. Make sure `rosgp` is running first
2. Wait 3-5 seconds before launching `rosd`
3. Check: `ros2 topic list` should show `/tf` and `/tf_static`

### Camera "queue is full" Error
**Symptom:** RViz shows "discarding message because the queue is full"
**Cause:** Frame mismatch (should be fixed now with static TF publisher)
**Fix:** Already fixed in spawn_robot.launch.py with static transform

### Gazebo Shows Wrong World
**Symptom:** See colored balls instead of ArUco poles (or vice versa)
**Cause:** Using wrong alias or Gazebo cached old world
**Fix:**
```bash
pkill -9 ruby
sleep 1
rosgp  # For marker world
# OR
rosg   # For test world with balls
```

---

## Alias Validation Status

✅ **rosb** - Validated, working correctly
✅ **rosd** - Validated, fixed to only launch RViz
✅ **rosgp** - Validated, launches marker world correctly
✅ **rosgu** - Validated, teleop GUI path correct
✅ **rosg** - Validated, launches test world (legacy/testing)
✅ **rosar** - Validated, ArUco detection launch file created

---

## Reload Aliases

After any changes to `~/.bashrc`, reload with:
```bash
source ~/.bashrc
# OR use the alias:
aliss
```
