#!/usr/bin/env python3
"""
Real-time IMU Data Analyzer
Subscribes to /imu/data topic and analyzes the data in real-time.
Saves results to CSV file for later analysis.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import csv
import time
from datetime import datetime
import math


class IMUAnalyzer(Node):
    def __init__(self):
        super().__init__('imu_analyzer')
        
        # Create subscriber
        self.subscription = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10)
        
        # Data storage
        self.data_points = []
        self.start_time = time.time()
        
        # Statistics
        self.count = 0
        self.sum_linear_acc = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.sum_angular_vel = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        
        # CSV file setup - always save as imu_data.csv (overwrites previous)
        self.csv_filename = 'imu_data.csv'
        self.csv_file = open(self.csv_filename, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        # Write CSV header
        self.csv_writer.writerow([
            'timestamp', 'elapsed_time',
            'linear_acc_x', 'linear_acc_y', 'linear_acc_z',
            'angular_vel_x', 'angular_vel_y', 'angular_vel_z',
            'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w'
        ])
        
        self.get_logger().info(f'IMU Analyzer started. Saving to {self.csv_filename}')
        self.get_logger().info('Press Ctrl+C to stop and see statistics')
    
    def imu_callback(self, msg):
        """Process incoming IMU messages"""
        self.count += 1
        elapsed = time.time() - self.start_time
        
        # Extract data
        lin_acc = msg.linear_acceleration
        ang_vel = msg.angular_velocity
        orient = msg.orientation
        
        # Update statistics
        self.sum_linear_acc['x'] += lin_acc.x
        self.sum_linear_acc['y'] += lin_acc.y
        self.sum_linear_acc['z'] += lin_acc.z
        
        self.sum_angular_vel['x'] += ang_vel.x
        self.sum_angular_vel['y'] += ang_vel.y
        self.sum_angular_vel['z'] += ang_vel.z
        
        # Save to CSV
        self.csv_writer.writerow([
            msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
            elapsed,
            lin_acc.x, lin_acc.y, lin_acc.z,
            ang_vel.x, ang_vel.y, ang_vel.z,
            orient.x, orient.y, orient.z, orient.w
        ])
        
        # Print every 10 messages (reduce console spam)
        if self.count % 10 == 0:
            self.get_logger().info(
                f'[{self.count}] Linear Acc: ({lin_acc.x:.3f}, {lin_acc.y:.3f}, {lin_acc.z:.3f}) m/s² | '
                f'Angular Vel: ({ang_vel.x:.3f}, {ang_vel.y:.3f}, {ang_vel.z:.3f}) rad/s'
            )
    
    def print_statistics(self):
        """Print final statistics"""
        if self.count == 0:
            self.get_logger().warn('No data received!')
            return
        
        # Calculate averages
        avg_lin_acc = {k: v / self.count for k, v in self.sum_linear_acc.items()}
        avg_ang_vel = {k: v / self.count for k, v in self.sum_angular_vel.items()}
        
        # Calculate magnitude
        lin_acc_mag = math.sqrt(sum(v**2 for v in avg_lin_acc.values()))
        ang_vel_mag = math.sqrt(sum(v**2 for v in avg_ang_vel.values()))
        
        print('\n' + '='*60)
        print('IMU DATA STATISTICS')
        print('='*60)
        print(f'Total messages received: {self.count}')
        print(f'Duration: {time.time() - self.start_time:.2f} seconds')
        print(f'\nAverage Linear Acceleration (m/s²):')
        print(f'  X: {avg_lin_acc["x"]:.6f}')
        print(f'  Y: {avg_lin_acc["y"]:.6f}')
        print(f'  Z: {avg_lin_acc["z"]:.6f}')
        print(f'  Magnitude: {lin_acc_mag:.6f}')
        print(f'\nAverage Angular Velocity (rad/s):')
        print(f'  X: {avg_ang_vel["x"]:.6f}')
        print(f'  Y: {avg_ang_vel["y"]:.6f}')
        print(f'  Z: {avg_ang_vel["z"]:.6f}')
        print(f'  Magnitude: {ang_vel_mag:.6f}')
        print(f'\nData saved to: {self.csv_filename}')
        print('='*60 + '\n')
    
    def cleanup(self):
        """Close CSV file"""
        self.csv_file.close()


def main(args=None):
    rclpy.init(args=args)
    analyzer = IMUAnalyzer()
    
    try:
        rclpy.spin(analyzer)
    except KeyboardInterrupt:
        print('\n\nStopping IMU analyzer...')
    finally:
        analyzer.print_statistics()
        analyzer.cleanup()
        analyzer.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
