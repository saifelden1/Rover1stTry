#!/usr/bin/env python3
"""
Simple GUI for controlling the robot with sliders
Uses tkinter for the GUI and publishes to /cmd_vel topic
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import tkinter as tk
from tkinter import ttk
import threading


class RobotTeleopGUI(Node):
    def __init__(self):
        super().__init__('robot_teleop_gui')
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.publish_velocity)
        
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        
        self.get_logger().info('Robot Teleop GUI Node Started')
    
    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = self.linear_velocity
        msg.angular.z = self.angular_velocity
        self.publisher.publish(msg)
    
    def set_linear(self, value):
        self.linear_velocity = float(value)
    
    def set_angular(self, value):
        self.angular_velocity = float(value)
    
    def stop(self):
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0


def create_gui(node):
    """Create the tkinter GUI"""
    root = tk.Tk()
    root.title("Robot Teleop Control")
    root.geometry("400x300")
    
    # Title
    title = tk.Label(root, text="Robot Velocity Control", font=("Arial", 16, "bold"))
    title.pack(pady=10)
    
    # Linear velocity slider
    linear_frame = tk.Frame(root)
    linear_frame.pack(pady=10, padx=20, fill='x')
    
    linear_label = tk.Label(linear_frame, text="Linear Velocity (m/s):", font=("Arial", 12))
    linear_label.pack()
    
    linear_value_label = tk.Label(linear_frame, text="0.00", font=("Arial", 10))
    linear_value_label.pack()
    
    linear_slider = tk.Scale(
        linear_frame,
        from_=-1.0,
        to=1.0,
        resolution=0.01,
        orient=tk.HORIZONTAL,
        length=300,
        command=lambda v: [node.set_linear(v), linear_value_label.config(text=f"{float(v):.2f}")]
    )
    linear_slider.set(0.0)
    linear_slider.pack()
    
    # Angular velocity slider
    angular_frame = tk.Frame(root)
    angular_frame.pack(pady=10, padx=20, fill='x')
    
    angular_label = tk.Label(angular_frame, text="Angular Velocity (rad/s):", font=("Arial", 12))
    angular_label.pack()
    
    angular_value_label = tk.Label(angular_frame, text="0.00", font=("Arial", 10))
    angular_value_label.pack()
    
    angular_slider = tk.Scale(
        angular_frame,
        from_=-2.0,
        to=2.0,
        resolution=0.01,
        orient=tk.HORIZONTAL,
        length=300,
        command=lambda v: [node.set_angular(v), angular_value_label.config(text=f"{float(v):.2f}")]
    )
    angular_slider.set(0.0)
    angular_slider.pack()
    
    # Stop button
    stop_button = tk.Button(
        root,
        text="STOP",
        font=("Arial", 14, "bold"),
        bg="red",
        fg="white",
        command=lambda: [node.stop(), linear_slider.set(0.0), angular_slider.set(0.0)]
    )
    stop_button.pack(pady=20)
    
    # Instructions
    instructions = tk.Label(
        root,
        text="Move sliders to control robot\nLinear: forward/backward | Angular: left/right rotation",
        font=("Arial", 9),
        fg="gray"
    )
    instructions.pack(pady=5)
    
    return root


def main():
    rclpy.init()
    node = RobotTeleopGUI()
    
    # Create GUI in main thread
    root = create_gui(node)
    
    # Run ROS2 spinning in separate thread
    def spin_node():
        rclpy.spin(node)
    
    ros_thread = threading.Thread(target=spin_node, daemon=True)
    ros_thread.start()
    
    # Run GUI main loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
