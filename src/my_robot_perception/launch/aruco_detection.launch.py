#!/usr/bin/env python3
"""
aruco_detection.launch.py - ArUco marker detection launch file

This launch file:
1. Launches the aruco_tracking node for marker detection
2. Configures marker dictionary (DICT_7X7_1000) and size (0.15m)
3. Remaps camera topics to match robot's camera
4. Publishes detected marker poses to TF tree

Use this alongside the Gazebo simulation (rosgp) to detect ArUco markers.
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # ArUco detection node
    # Uses aruco_tracking package to detect markers from camera feed
    aruco_node = Node(
        package='aruco_tracking',
        executable='aruco_node',
        name='aruco_detection',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'arucoDictType': 7,  # DICT_7X7_1000 (matches marker poles)
            'markerSize': 0.15,  # 15cm markers (matches pole markers)
        }],
        remappings=[
            # Remap aruco_tracking's expected topics to robot's camera topics
            ('/image_raw', '/camera/image_raw'),
            ('/camera/color/camera_info', '/camera/camera_info'),
        ]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time'
        ),
        aruco_node
    ])
