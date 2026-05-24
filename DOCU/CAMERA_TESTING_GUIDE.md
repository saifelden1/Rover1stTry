# Camera Sensor Testing Guide

This guide shows you how to test and visualize the camera sensor on your robot.

## Prerequisites

Make sure the simulation is running before testing the camera.

## Step-by-Step Testing Instructions

### Step 1: Launch the Robot Simulation

Open a **new terminal** and run:

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch my_robot_description gazebo.launch.py
```

**What you should see:**
- Gazebo window opens
- Robot spawns in the simulation
- Robot has a small black box (camera) on the front

**Wait 5-10 seconds** for everything to initialize before proceeding.

---

### Step 2: Check Camera Topics Exist

Open a **second terminal** and run:

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 topic list | grep camera
```

**Expected output:**
```
/camera/camera_info
/camera/image_raw
```

If you see these two topics, the camera is working! ✅

---

### Step 3: Check Camera Publishing Rate

In the same terminal, check how fast the camera is publishing:

```bash
ros2 topic hz /camera/image_raw
```

**Expected output:**
```
average rate: 30.xxx
```

The rate should be around **30 Hz** (30 frames per second).

Press `Ctrl+C` to stop.

---

### Step 4: View Camera Info

Check the camera calibration information:

```bash
ros2 topic echo /camera/camera_info --once
```

**Expected output:**
You should see camera parameters including:
- `width: 640`
- `height: 480`
- `distortion_model`
- `k: [...]` (camera matrix)

---

### Step 5: Visualize Camera in RViz

Open a **third terminal** and launch RViz:

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch my_robot_description display.launch.py
```

**In RViz:**
1. You should see the robot model with the camera (black box on front)
2. Look for the **Camera** display in the left panel
3. The camera view should show what the robot sees
4. You can also see the **camera_link** frame in the TF display

---

### Step 6: View Camera Image with rqt_image_view

For a dedicated image viewer, open a **fourth terminal**:

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
rqt_image_view
```

**In the rqt_image_view window:**
1. Click the dropdown menu at the top
2. Select `/camera/image_raw`
3. You should see the live camera feed from the robot

**What you should see:**
- The ground plane (gray)
- Parts of the robot if the camera angle captures them
- The environment around the robot

---

### Step 7: Run Automated Verification Script

Use the provided Python script to verify everything automatically:

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 verify_camera.py
```

**Expected output:**
```
[INFO] Camera verifier started. Listening for camera data...
[INFO] ✓ First image received: 640x480, encoding=rgb8
[INFO] ✓ First camera_info received: 640x480
============================================================
Camera Statistics (after 5.0s):
  Images received: 150 (30.0 Hz)
  CameraInfo received: 150 (30.0 Hz)
============================================================
[INFO] ✓ Image rate is within expected range (25-35 Hz)
[INFO] ✓ CameraInfo rate is within expected range (25-35 Hz)
```

---

## Quick Test Script

For a fast check, run the quick test script:

```bash
cd ~/Desktop/ROARTASK
./test_camera_quick.sh
```

This will automatically check topics, info, and frequency.

---

## Troubleshooting

### Camera topics don't exist

**Problem:** `ros2 topic list | grep camera` shows nothing

**Solutions:**
1. Make sure Gazebo simulation is running
2. Wait 10-15 seconds after launching for topics to appear
3. Check if the robot spawned correctly in Gazebo
4. Rebuild the workspace:
   ```bash
   cd ~/Desktop/ROARTASK/ros2_ws
   colcon build --packages-select my_robot_description
   source install/setup.bash
   ```

### Camera rate is 0 Hz

**Problem:** `ros2 topic hz` shows no messages

**Solutions:**
1. Check if Gazebo is paused (click the play button ▶️ in Gazebo)
2. Make sure the simulation is running (not frozen)
3. Restart the simulation

### RViz doesn't show camera view

**Problem:** Camera display is black or shows error

**Solutions:**
1. Make sure the Camera display is enabled (checkbox in left panel)
2. Check that the topic is set to `/camera/image_raw`
3. Try changing the "Image Rendering" option to "background and overlay"
4. Restart RViz

### rqt_image_view shows no image

**Problem:** Window is black or shows "No image"

**Solutions:**
1. Make sure you selected `/camera/image_raw` from the dropdown
2. Check that camera topics are publishing (`ros2 topic hz /camera/image_raw`)
3. Try closing and reopening rqt_image_view

---

## What the Camera Should See

The camera is positioned:
- **On the front face** of the robot base (centered)
- **Pitched down 15°** to view the ground
- **Black box** visible in both RViz and Gazebo

So the camera view should show:
- The ground plane in front of the robot
- Any objects or markers in front of the robot
- The view is angled down toward the ground

---

## Camera Specifications

- **Resolution:** 640×480 pixels
- **Format:** RGB8 (color)
- **Field of View:** 60° horizontal
- **Update Rate:** 30 Hz
- **Topics:**
  - `/camera/image_raw` - Raw image data
  - `/camera/camera_info` - Camera calibration info

---

## Next Steps

Once you've verified the camera works:
1. ✅ Camera topics exist and publish at 30 Hz
2. ✅ Camera image can be visualized in RViz or rqt_image_view
3. ✅ Camera info contains correct resolution (640×480)

You're ready to move on to creating the Gazebo world with ArUco markers!

---

## Summary of Commands

```bash
# Terminal 1: Launch simulation
ros2 launch my_robot_description gazebo.launch.py

# Terminal 2: Check topics
ros2 topic list | grep camera
ros2 topic hz /camera/image_raw
ros2 topic echo /camera/camera_info --once

# Terminal 3: Launch RViz
ros2 launch my_robot_description display.launch.py

# Terminal 4: View camera image
rqt_image_view

# Or run automated test
python3 verify_camera.py
```
