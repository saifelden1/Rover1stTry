#!/usr/bin/env python3
"""
gazebo.launch.py - Gazebo simulation launch file

This launch file:
1. Processes the xacro file into URDF
2. Launches Gazebo Ignition with empty world
3. Launches robot_state_publisher with use_sim_time=true
4. Spawns robot at origin using spawn_entity service

Use this to test the robot in Gazebo simulation.
"""

import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import xacro


def generate_launch_description():
    
    # Get the package share directory
    pkg_share = FindPackageShare('my_robot_description').find('my_robot_description')
    
    # Path to the xacro file
    xacro_file = os.path.join(pkg_share, 'urdf', 'my_robot.urdf.xacro')
    
    # Process the xacro file to generate URDF
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}
    
    # Robot State Publisher Node
    # Publishes TF transforms for all robot links based on URDF
    # use_sim_time=true ensures synchronization with Gazebo clock
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            robot_description,
            {'use_sim_time': True}
        ]
    )
    
    # Gazebo Launch
    # Launches Gazebo Ignition with custom world that includes Sensors system
    world_file = os.path.join(pkg_share, 'worlds', 'empty_with_sensors.sdf')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(FindPackageShare('ros_gz_sim').find('ros_gz_sim'),
                        'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={
            'gz_args': ['-r ', world_file],
            'on_exit_shutdown': 'true'
        }.items()
    )
    
    # Spawn Robot Entity
    # Uses spawn_entity service to place robot in Gazebo at origin
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'my_robot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.2'  # Spawn slightly above ground to prevent initial collision
        ],
        output='screen'
    )
    
    # Bridge between Ignition Gazebo and ROS 2
    # This bridges the /cmd_vel, /odom, /imu/data, and camera topics
    # Note: Gazebo Sim 8 (Harmonic) uses scoped topic names for sensors
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@ignition.msgs.Odometry',
            '/imu/data@sensor_msgs/msg/Imu@ignition.msgs.IMU',
            '/world/empty/model/my_robot/link/camera_link/sensor/camera/image@sensor_msgs/msg/Image[ignition.msgs.Image',
            '/world/empty/model/my_robot/link/camera_link/sensor/camera/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo',
        ],
        remappings=[
            ('/world/empty/model/my_robot/link/camera_link/sensor/camera/image', '/camera/image_raw'),
            ('/world/empty/model/my_robot/link/camera_link/sensor/camera/camera_info', '/camera/camera_info'),
        ],
        output='screen'
    )
    
    # Launch Description
    return LaunchDescription([
        gazebo,
        robot_state_publisher_node,
        spawn_entity,
        bridge
    ])
