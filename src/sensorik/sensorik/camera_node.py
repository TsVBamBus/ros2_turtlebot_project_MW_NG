import rclpy
from rclpy.node import Node

from sensorik.aruco_erkennung import ArucoErkennung


class CameraNode(Node):
    
    def __init__(self):
        super().__init__('camera_node')
        self.logik = ArucoErkennung()

        # TODO: create_publisher(ArucoMarker, ...)
        self.pub_marker = None

        # TODO: create_timer(..., self.timer_callback)
        self.timer = None

        self.get_logger().info('camera_node gestartet')

    def timer_callback(self):
        return


def main():
    rclpy.init()
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
