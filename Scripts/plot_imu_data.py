#!/usr/bin/env python3
"""
IMU Data Plotter and Analyzer
Reads imu_data.csv and creates visualization plots with analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def analyze_and_plot_imu(csv_file='imu_data.csv'):
    """Load, analyze, and plot IMU data"""
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        print("Please run imu_realtime_analyzer.py first to collect data.")
        sys.exit(1)
    
    # Load data
    print(f"Loading data from {csv_file}...")
    df = pd.read_csv(csv_file)
    
    if len(df) == 0:
        print("Error: CSV file is empty!")
        sys.exit(1)
    
    print(f"Loaded {len(df)} data points")
    print(f"Duration: {df['elapsed_time'].max():.2f} seconds")
    
    # Calculate statistics
    print("\n" + "="*60)
    print("IMU DATA ANALYSIS")
    print("="*60)
    
    print("\nLinear Acceleration Statistics (m/s²):")
    print(f"  X-axis: mean={df['linear_acc_x'].mean():.6f}, std={df['linear_acc_x'].std():.6f}")
    print(f"  Y-axis: mean={df['linear_acc_y'].mean():.6f}, std={df['linear_acc_y'].std():.6f}")
    print(f"  Z-axis: mean={df['linear_acc_z'].mean():.6f}, std={df['linear_acc_z'].std():.6f}")
    
    print("\nAngular Velocity Statistics (rad/s):")
    print(f"  X-axis: mean={df['angular_vel_x'].mean():.6f}, std={df['angular_vel_x'].std():.6f}")
    print(f"  Y-axis: mean={df['angular_vel_y'].mean():.6f}, std={df['angular_vel_y'].std():.6f}")
    print(f"  Z-axis: mean={df['angular_vel_z'].mean():.6f}, std={df['angular_vel_z'].std():.6f}")
    
    # Calculate magnitudes
    df['linear_acc_magnitude'] = np.sqrt(
        df['linear_acc_x']**2 + 
        df['linear_acc_y']**2 + 
        df['linear_acc_z']**2
    )
    
    df['angular_vel_magnitude'] = np.sqrt(
        df['angular_vel_x']**2 + 
        df['angular_vel_y']**2 + 
        df['angular_vel_z']**2
    )
    
    print(f"\nMagnitudes:")
    print(f"  Linear Acceleration: mean={df['linear_acc_magnitude'].mean():.6f} m/s²")
    print(f"  Angular Velocity: mean={df['angular_vel_magnitude'].mean():.6f} rad/s")
    print("="*60 + "\n")
    
    # Create plots
    print("Generating plots...")
    
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    fig.suptitle('IMU Data Analysis', fontsize=16, fontweight='bold')
    
    # Convert to numpy arrays for plotting
    time = df['elapsed_time'].values
    
    # Plot 1: Linear Acceleration (X, Y, Z)
    ax = axes[0, 0]
    ax.plot(time, df['linear_acc_x'].values, label='X', alpha=0.7)
    ax.plot(time, df['linear_acc_y'].values, label='Y', alpha=0.7)
    ax.plot(time, df['linear_acc_z'].values, label='Z', alpha=0.7)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Linear Acceleration (m/s²)')
    ax.set_title('Linear Acceleration (X, Y, Z)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Linear Acceleration Magnitude
    ax = axes[0, 1]
    ax.plot(time, df['linear_acc_magnitude'].values, color='purple', linewidth=1.5)
    ax.axhline(y=9.81, color='r', linestyle='--', label='Gravity (9.81 m/s²)', alpha=0.7)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Magnitude (m/s²)')
    ax.set_title('Linear Acceleration Magnitude')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Angular Velocity (X, Y, Z)
    ax = axes[1, 0]
    ax.plot(time, df['angular_vel_x'].values, label='X (Roll)', alpha=0.7)
    ax.plot(time, df['angular_vel_y'].values, label='Y (Pitch)', alpha=0.7)
    ax.plot(time, df['angular_vel_z'].values, label='Z (Yaw)', alpha=0.7)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Angular Velocity (rad/s)')
    ax.set_title('Angular Velocity (X, Y, Z)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Angular Velocity Magnitude
    ax = axes[1, 1]
    ax.plot(time, df['angular_vel_magnitude'].values, color='orange', linewidth=1.5)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Magnitude (rad/s)')
    ax.set_title('Angular Velocity Magnitude')
    ax.grid(True, alpha=0.3)
    
    # Plot 5: Linear Acceleration Distribution (Histogram)
    ax = axes[2, 0]
    ax.hist(df['linear_acc_x'].values, bins=50, alpha=0.5, label='X', color='blue')
    ax.hist(df['linear_acc_y'].values, bins=50, alpha=0.5, label='Y', color='orange')
    ax.hist(df['linear_acc_z'].values, bins=50, alpha=0.5, label='Z', color='green')
    ax.set_xlabel('Linear Acceleration (m/s²)')
    ax.set_ylabel('Frequency')
    ax.set_title('Linear Acceleration Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 6: Angular Velocity Distribution (Histogram)
    ax = axes[2, 1]
    ax.hist(df['angular_vel_x'].values, bins=50, alpha=0.5, label='X', color='blue')
    ax.hist(df['angular_vel_y'].values, bins=50, alpha=0.5, label='Y', color='orange')
    ax.hist(df['angular_vel_z'].values, bins=50, alpha=0.5, label='Z', color='green')
    ax.set_xlabel('Angular Velocity (rad/s)')
    ax.set_ylabel('Frequency')
    ax.set_title('Angular Velocity Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    output_file = 'imu_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Plot saved as: {output_file}")
    
    # Show plot
    print("Displaying plot... (close window to exit)")
    plt.show()
    
    print("\nAnalysis complete!")


if __name__ == '__main__':
    # Check if custom filename provided
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = 'imu_data.csv'
    
    analyze_and_plot_imu(csv_file)
