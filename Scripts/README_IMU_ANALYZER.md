# IMU Real-Time Analyzer - QUICK START

## 3-Step Process

### 1. Start Simulation
```bash
rosgp
```

### 2. Record Data (new terminal)
```bash
cd ~/Desktop/ROARTASK/Scripts
python3 imu_realtime_analyzer.py
```
Run for 10-30 seconds, then **Ctrl+C**

### 3. Plot Results
```bash
python3 plot_imu_data.py
```

## What You Get

**Files created:**
- `imu_data.csv` - Raw IMU data
- `imu_analysis.png` - 6 visualization plots

**Terminal shows:**
- Statistics (mean, std deviation)
- Magnitudes
- Data quality metrics

## Full Documentation

See `HOW_TO_USE_IMU.md` for detailed instructions.
