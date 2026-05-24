# How to Use IMU Data Collection and Analysis

## Simple 3-Step Process

### Step 1: Start Simulation

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source install/setup.bash
rosgp
```

### Step 2: Record IMU Data

Open a **new terminal**:

```bash
cd ~/Desktop/ROARTASK/ros2_ws
source install/setup.bash
cd ~/Desktop/ROARTASK/Scripts
python3 imu_realtime_analyzer.py
```

**Let it run for 10-30 seconds**, then press **Ctrl+C** to stop.

This creates: `imu_data.csv` in the Scripts folder.

### Step 3: Plot and Analyze

```bash
python3 plot_imu_data.py
```

This will:
- Print statistics to terminal
- Create `imu_analysis.png` with 6 plots
- Show interactive plot window

## What You Get

### Terminal Output:
- Mean and standard deviation for all axes
- Linear acceleration statistics
- Angular velocity statistics
- Magnitude calculations

### Plots (imu_analysis.png):
1. **Linear Acceleration (X, Y, Z)** - Shows acceleration over time
2. **Linear Acceleration Magnitude** - Total acceleration with gravity reference
3. **Angular Velocity (X, Y, Z)** - Rotation rates over time
4. **Angular Velocity Magnitude** - Total rotation rate
5. **Linear Acceleration Distribution** - Histogram showing data spread
6. **Angular Velocity Distribution** - Histogram showing rotation spread

## Optional: Move the Robot

To see more interesting data, move the robot while recording:

**Terminal 3** (while recording):
```bash
cd ~/Desktop/ROARTASK/ros2_ws
source install/setup.bash

# Move forward and rotate
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.5}}" -r 10
```

Press **Ctrl+C** to stop movement.

## Tips

✅ **Stationary robot**: Z-axis should show ~9.8 m/s² (gravity)  
✅ **Moving robot**: X and Y will show acceleration changes  
✅ **Rotating robot**: Angular velocity Z will be non-zero  
✅ **Run for 10+ seconds**: Get better statistics  

## File Locations

All files are in: `~/Desktop/ROARTASK/Scripts/`

- `imu_data.csv` - Raw data (overwritten each time)
- `imu_analysis.png` - Visualization (overwritten each time)
- `imu_realtime_analyzer.py` - Recording script
- `plot_imu_data.py` - Plotting script

## Troubleshooting

**No data received?**
- Make sure simulation is running (`rosgp`)
- Check topic exists: `ros2 topic list | grep imu`
- Check data is publishing: `ros2 topic echo /imu/data --once`

**Plot doesn't show?**
- Make sure you ran the recording script first
- Check `imu_data.csv` exists and has data
- Install matplotlib: `pip3 install matplotlib pandas numpy`
