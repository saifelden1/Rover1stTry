import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import numpy as np

class FakeCamera(Node):
    def __init__(self):
        super().__init__('fake_camera')
        self.image_pub = self.create_publisher(Image, '/image_raw', 10)
        self.info_pub = self.create_publisher(CameraInfo, '/camera/color/camera_info', 10)
        self.timer = self.create_timer(0.1, self.timer_callback) # 10 Hz
        self.bridge = CvBridge()

        # 1. Create a blank white image (640x480)
        self.img = np.ones((480, 640, 3), dtype=np.uint8) * 255

        # 2. Draw ArUco Marker (ID 0, Dict 5x5_100)
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
        # Compatibility check for OpenCV versions
        try:
            # Try new OpenCV (4.7+)
            marker_img = cv2.aruco.generateImageMarker(aruco_dict, 26, 200)
        except AttributeError:
            # Fallback to old OpenCV (4.6 and older)
            marker_img = cv2.aruco.drawMarker(aruco_dict, 26, 200)

        marker_img = cv2.cvtColor(marker_img, cv2.COLOR_GRAY2BGR)

        # 3. Paste it in the center
        x_offset = (640 - 200) // 2
        y_offset = (480 - 200) // 2
        self.img[y_offset:y_offset+200, x_offset:x_offset+200] = marker_img

        self.get_logger().info("Fake Camera Initialized - Publishing Marker ID 26")

    def timer_callback(self):
        # Publish Image
        msg = self.bridge.cv2_to_imgmsg(self.img, encoding="bgr8")
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "camera_optical_frame"
        self.image_pub.publish(msg)

        # Publish Camera Info
        info_msg = CameraInfo()
        info_msg.header = msg.header
        info_msg.width = 640
        info_msg.height = 480
        info_msg.k = [600.0, 0.0, 320.0, 0.0, 600.0, 240.0, 0.0, 0.0, 1.0]
        info_msg.d = [0.0, 0.0, 0.0, 0.0, 0.0] 
        self.info_pub.publish(info_msg)

def main():
    rclpy.init()
    node = FakeCamera()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
