#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
import cv2
import numpy as np

if not hasattr(np, 'float'):
    np.float = float
    
import tf_transformations 
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker, MarkerArray

from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose

from cv_bridge import CvBridge
from aruco_tracking.aruco_tracker import ArucoTracker

class ArucoTrackingNode(Node):
    def __init__(self):
        super().__init__('aruco_tracking_node')
        self.bridge = CvBridge()
        
        self.declare_parameter('cameraTopic', '/image_raw')
        self.declare_parameter('arucoDictType', 7) 
        self.declare_parameter('visualize', False)
        self.declare_parameter('markerSize', 0.15)
        
        self.camera_topic = self.get_parameter('cameraTopic').value
        self.aruco_dict_type = self.get_parameter('arucoDictType').value
        self.visualize = self.get_parameter('visualize').value
        self.marker_size = self.get_parameter('markerSize').value

        self.get_logger().info(f"Looking for Marker Dictionary: {self.aruco_dict_type}")
        self.get_logger().info(f"Listening to Topic: {self.camera_topic}")

        self.aruco_tracker = ArucoTracker(self.aruco_dict_type)
        self.camera_matrix = None
        self.dist_coeffs = None
        
        self.backup_camera_matrix = np.array([[659.3, 0.0, 659.3], [0.0, 659.3, 371.4], [0.0, 0.0, 1.0]])
        self.backup_dist_coeffs = np.array([-0.04, 0.009, -0.004, 0.0001, -0.0003])

        self.create_subscription(Image, self.camera_topic, self.image_callback, qos_profile_sensor_data)
        self.create_subscription(CameraInfo, '/camera/color/camera_info', self.info_callback, 10)
        
        self.marker_pub = self.create_publisher(MarkerArray, "/aruco_markers", 10)
        self.debug_pub = self.create_publisher(Image, "/aruco_debug", 10)        

        self.box_pub = self.create_publisher(Detection2DArray, "/perception/detected_aruco", 10)
        
        self.get_logger().info("NODE STARTED SUCCESSFULLY")

    def info_callback(self, msg):
        self.camera_matrix = np.array(msg.k).reshape(3, 3)
        self.dist_coeffs = np.array(msg.d)

    def image_callback(self, image_msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"CV_BRIDGE ERROR: {e}")
            return

        corners, ids, rejected = self.aruco_tracker.detectMarkers(cv_image)

        box_msg = Detection2DArray()
        box_msg.header = image_msg.header

        marker_array = MarkerArray()

        if ids is not None:
            self.get_logger().info(f"FOUND MARKER ID: {ids[0]}") 
            
            cam_mat = self.camera_matrix if self.camera_matrix is not None else self.backup_camera_matrix
            dist = self.dist_coeffs if self.dist_coeffs is not None else self.backup_dist_coeffs
            rvecs, tvecs = self.aruco_tracker.estimatePose(corners, self.marker_size, cam_mat, dist)

            if self.visualize:
                cv_image = self.aruco_tracker.drawMarkers(cv_image, corners, ids, rvecs, tvecs, cam_mat, dist)

            for i in range(len(ids)):
                rvec, tvec = rvecs[i].flatten(), tvecs[i].flatten()
                rotation_matrix, _ = cv2.Rodrigues(rvec)
                transform_matrix = np.identity(4)
                transform_matrix[:3, :3] = rotation_matrix
                quaternion = tf_transformations.quaternion_from_matrix(transform_matrix)

                marker = Marker()
                marker.header = image_msg.header
                marker.ns = "aruco_markers"
                marker.id = int(ids[i][0])
                marker.type = Marker.CUBE
                marker.action = Marker.ADD
                marker.pose.position.x = float(tvec[0])
                marker.pose.position.y = float(tvec[1])
                marker.pose.position.z = float(tvec[2])
                marker.pose.orientation.x = quaternion[0]
                marker.pose.orientation.y = quaternion[1]
                marker.pose.orientation.z = quaternion[2]
                marker.pose.orientation.w = quaternion[3]
                marker.scale.x = self.marker_size
                marker.scale.y = self.marker_size
                marker.scale.z = 0.01
                marker.color.r = 0.0
                marker.color.g = 1.0
                marker.color.b = 0.0
                marker.color.a = 0.8
                
                text_marker = Marker()
                text_marker.header = image_msg.header
                text_marker.ns = "aruco_ids"
                text_marker.id = int(ids[i][0]) + 1000
                text_marker.type = Marker.TEXT_VIEW_FACING
                text_marker.action = Marker.ADD
                text_marker.pose.position.x = float(tvec[0])
                text_marker.pose.position.y = float(tvec[1])
                text_marker.pose.position.z = float(tvec[2]) - 0.15
                text_marker.pose.orientation.w = 1.0
                text_marker.scale.z = 0.1
                text_marker.color.r = 1.0
                text_marker.color.g = 1.0
                text_marker.color.b = 1.0
                text_marker.color.a = 1.0
                text_marker.text = f"ID: {ids[i][0]}"

                marker_array.markers.append(marker)
                marker_array.markers.append(text_marker)

                c = corners[i][0]
                x_coords = c[:, 0]
                y_coords = c[:, 1]
                
                width = np.max(x_coords) - np.min(x_coords)
                height = np.max(y_coords) - np.min(y_coords)
                center_x = np.min(x_coords) + (width / 2.0)
                center_y = np.min(y_coords) + (height / 2.0)

                det_2d = Detection2D()
                det_2d.id = str(ids[i][0])
                det_2d.header = image_msg.header
                det_2d.bbox.center.position.x = float(center_x)
                det_2d.bbox.center.position.y = float(center_y)
                det_2d.bbox.size_x = float(width)
                det_2d.bbox.size_y = float(height)

                hyp = ObjectHypothesisWithPose()
                hyp.hypothesis.class_id = "aruco_marker"
                hyp.hypothesis.score = 1.0
                det_2d.results.append(hyp)

                box_msg.detections.append(det_2d)

        self.box_pub.publish(box_msg)
        self.marker_pub.publish(marker_array)

        if self.visualize:
            debug_msg = self.bridge.cv2_to_imgmsg(cv_image, "bgr8")
            debug_msg.header = image_msg.header
            self.debug_pub.publish(debug_msg)
            cv2.imshow("ArUco Debug", cv_image)
            cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = ArucoTrackingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()