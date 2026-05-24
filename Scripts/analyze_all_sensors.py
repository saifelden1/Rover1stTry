#!/usr/bin/env python3
"""
Master Sensor Analyzer
Runs both IMU and Camera analyzers simultaneously.
"""

import rclpy
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import Imu, Image, CameraInfo
from cv_bridge import CvBridge
import csv
import time
from datetime import datetime
import os
import cv2
import math


class MasterSensorAnalyzer(rclpy.node.Node):
    def __init__(self):
        super().__init__('master_sensor_analyzer')
        
        # CV Bridge
        self.bridge = CvBridge()
        
        # Subscribers
        self.imu_sub = self.create_subscription(Imu, '/imu/data', self.imu_callback, 10)
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.info_sub = self.create_subscription(CameraInfo, '/camera/camera_info', self.info_callback, 10)
        
        # Data counters
        self.start_time = time.time()
        self.imu_count = 0
        self.image_count = 0
        self.camera_info = None
        
        # IMU statistics
        self.sum_linear_acc = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.sum_angular_vel = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f'sensor_data_{timestamp}'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # CSV files
        self.imu_csv = open(os.path.join(self.output_dir, 'imu_data.csv'), 'w', newline='')
        self.imu_writer = csv.writer(self.imu_csv)
        self.imu_writer.writerow([
            'timestamp', 'elapsed_time',
            'linear_acc_x', 'linear_acc_y', 'linear_acc_z',
            'angular_vel_x', 'angular_vel_y', 'angular_vel_z'
        ])
        
        self.camera_csv = open(os.path.join(self.output_dir, 'camera_data.csv'), 'w', newline='')
        self.camera_writer = csv.writer(self.camera_csv)
        self.camera_writer.writerow([
            'frame_number', 'timestamp', 'elapsed_time',
            'mean_brightness', 'std_brightness'
        ])
        
        self.get_logger().info(f'Master Analyzer started. Saving to {self.output_dir}/')
        self.get_logger().info('Collecting data from IMU and Camera...')
        self.get_logger().info('Press Ctrl+C to stop')
    
    def imu_callback(self, msg):
        self.imu_count += 1
        elapsed = time.time() - self.start_time
        
        lin_acc = msg.linear_acceleration
        ang_vel = msg.angular_velocity
        
        self.sum_linear_acc['x'] += lin_acc.x
        self.sum_linear_acc['y'] += lin_acc.y
        self.sum_linear_acc['z'] += lin_acc.z
        
        self.sum_angular_vel['x'] += ang_vel.x
        self.sum_angular_vel['y'] += ang_vel.y
        self.sum_angular_vel['z'] += ang_vel.z
        
        self.imu_writer.writerow([
            msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
            elapsed,
            lin_acc.x, lin_acc.y, lin_acc.z,
            ang_vel.x, ang_vel.y, ang_vel.z
        ])
        
        if self.imu_count % 50 == 0:
            self.get_logger().info(f'IMU: {self.imu_count} messages | Camera: {self.image_count} frames')
    
    def image_callback(self, msg):
        self.image_count += 1
        elapsed = time.time() - self.start_time
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            mean_brightness = gray.mean()
            std_brightness = gray.std()
            
            self.camera_writer.writerow([
                self.image_count,
                msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9,
                elapsed,
                mean_brightness, std_brightness
            ])
            
            # Save sample images every 30 frames
            if self.image_count % 30 == 0:
                filename = os.path.join(self.output_dir, f'frame_{self.image_count:04d}.jpg')
                cv2.imwrite(filename, cv_image)
        
        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')
    
    def info_callback(self, msg):
        if self.camera_info is None:
            self.camera_info = msg
    
    def print_statistics(self):
        duration = time.time() - self.start_time
        
        print('\n' + '='*60)
        print('SENSOR DATA COLLECTION COMPLETE')
        print('='*60)
        print(f'Duration: {duration:.2f} seconds')
        print(f'\nIMU Data:')
        print(f'  Messages: {self.imu_count}')
        print(f'  Rate: {self.imu_count/duration:.1f} Hz')
        
        if self.imu_count > 0:
            avg_lin = {k: v/self.imu_count for k, v in self.sum_linear_acc.items()}
            avg_ang = {k: v/self.imu_count for k, v in self.sum_angular_vel.items()}
            print(f'  Avg Linear Acc: ({avg_lin["x"]:.3f}, {avg_lin["y"]:.3f}, {avg_lin["z"]:.3f}) m/s²')
            print(f'  Avg Angular Vel: ({avg_ang["x"]:.3f}, {avg_ang["y"]:.3f}, {avg_ang["z"]:.3f}) rad/s')
        
        print(f'\nCamera Data:')
        print(f'  Frames: {self.image_count}')
        print(f'  Rate: {self.image_count/duration:.1f} FPS')
        print(f'  Saved images: {self.image_count // 30}')
        
        print(f'\nAll data saved to: {self.output_dir}/')
        print('='*60 + '\n')
    
    def cleanup(self):
        self.imu_csv.close()
        self.camera_csv.close()


def main(args=None):
    rclpy.init(args=args)
    analyzer = MasterSensorAnalyzer()
    
    try:
        rclpy.spin(analyzer)
    except KeyboardInterrupt:
        print('\n\nStopping analyzer...')
    finally:
        analyzer.print_statistics()
        analyzer.cleanup()
        analyzer.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
