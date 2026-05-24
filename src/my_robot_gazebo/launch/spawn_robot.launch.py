#!/usr/bin/env python3
"""
Launch file for spawning the robot in the custom marker world.

This launch file:
1. Processes the robot URDF from xacro
2. Launches Gazebo Ignition with the marker_world.world
3. Launches robot_state_publisher with the processed URDF
4. Spawns the robot at the origin (0, 0, 0.1) facing +X axis
5. Sets use_sim_time:=true for all nodes

The robot is positioned at the center of the 6m x 6m square formed by the marker poles,
ensuring at least 2 markers are visible in the camera view.
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Get package paths
    pkg_my_robot_description = get_package_share_directory('my_robot_description')
    pkg_my_robot_gazebo = get_package_share_directory('my_robot_gazebo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    
    # Set Gazebo model path to include workspace models directory (local, not global)
    workspace_models_path = os.path.join(pkg_my_robot_gazebo, 'models')
    if 'GZ_SIM_RESOURCE_PATH' in os.environ:
        os.environ['GZ_SIM_RESOURCE_PATH'] = os.environ['GZ_SIM_RESOURCE_PATH'] + ':' + workspace_models_path
    else:
        os.environ['GZ_SIM_RESOURCE_PATH'] = workspace_models_path
    
    # Process xacro file to generate URDF
    xacro_file = os.path.join(pkg_my_robot_description, 'urdf', 'my_robot.urdf.xacro')
    robot_description_content = Command(['xacro ', xacro_file])
    robot_description = ParameterValue(robot_description_content, value_type=str)
    
    # World file path
    world_file = os.path.join(pkg_my_robot_gazebo, 'worlds', 'marker_world.world')
    
    # Debug: Print paths to verify correct loading
    print(f"[spawn_robot.launch.py] Loading world: {world_file}")
    print(f"[spawn_robot.launch.py] Models path: {workspace_models_path}")
    print(f"[spawn_robot.launch.py] GZ_SIM_RESOURCE_PATH: {os.environ.get('GZ_SIM_RESOURCE_PATH', 'NOT SET')}")
    
    # Verify world file exists
    if not os.path.exists(world_file):
        raise FileNotFoundError(f"World file not found: {world_file}")
    
    # Launch Gazebo Ignition with custom world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': ['-r ', world_file],  # -r flag runs simulation immediately
            'on_exit_shutdown': 'true'
        }.items()
    )
    
    # Robot state publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description
        }]
    )
    
    # Spawn robot at origin (0, 0, 0.1) facing +X axis
    # Position ensures robot is centered in the marker square with good visibility
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_robot',
        output='screen',
        arguments=[
            '-name', 'my_robot',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1',
            '-Y', '0.0'  # Yaw = 0 (facing +X axis)
        ]
    )
    
    # Bridge for IMU data: Gazebo topic -> ROS 2 topic
    # Using wildcard pattern to match any world/model structure
    bridge_imu = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_imu',
        output='screen',
        arguments=[
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU'
        ],
        remappings=[
            ('/imu', '/imu/data')
        ],
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # Bridge for cmd_vel: ROS 2 topic -> Gazebo topic (bidirectional)
    bridge_cmd_vel = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_cmd_vel',
        output='screen',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist'
        ],
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # Bridge for odometry: Gazebo topic -> ROS 2 topic
    bridge_odom = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_odom',
        output='screen',
        arguments=[
            '/model/my_robot/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry'
        ],
        remappings=[
            ('/model/my_robot/odometry', '/odom')
        ],
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # Bridge for camera image: Gazebo topic -> ROS 2 topic
    bridge_camera_image = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_camera_image',
        output='screen',
        arguments=[
            '/world/marker_world/model/my_robot/link/camera_link/sensor/camera/image@sensor_msgs/msg/Image[gz.msgs.Image'
        ],
        remappings=[
            ('/world/marker_world/model/my_robot/link/camera_link/sensor/camera/image', '/camera/image_raw')
        ],
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # Bridge for camera info: Gazebo topic -> ROS 2 topic
    bridge_camera_info = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_camera_info',
        output='screen',
        arguments=[
            '/world/marker_world/model/my_robot/link/camera_link/sensor/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'
        ],
        remappings=[
            ('/world/marker_world/model/my_robot/link/camera_link/sensor/camera/camera_info', '/camera/camera_info')
        ],
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # Bridge for joint states: Gazebo topic -> ROS 2 topic
    bridge_joint_states = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge_joint_states',
        output='screen',
        arguments=[
            '/world/marker_world/model/my_robot/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'
        ],
        remappings=[
            ('/world/marker_world/model/my_robot/joint_state', '/joint_states')
        ],
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    # Static transform publisher to fix camera frame naming
    # Gazebo publishes camera data with frame 'my_robot/camera_link/camera'
    # but TF tree has 'camera_link', so we create an identity transform
    static_tf_camera = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='camera_frame_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'camera_link', 'my_robot/camera_link/camera'],
        parameters=[{
            'use_sim_time': use_sim_time
        }]
    )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time'
        ),
        gazebo,
        robot_state_publisher,
        # Delay robot spawn to ensure Gazebo is fully loaded
        TimerAction(
            period=3.0,
            actions=[spawn_robot]
        ),
        bridge_imu,
        bridge_cmd_vel,
        bridge_odom,
        bridge_camera_image,
        bridge_camera_info,
        bridge_joint_states,
        static_tf_camera
    ])
