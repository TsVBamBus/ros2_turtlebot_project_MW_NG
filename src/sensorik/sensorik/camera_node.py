import rclpy
from rclpy.node import Node

class CameraNode(Node):

    def __init__(self):
        super().__init__("camera_node")
        self.get_logger().info("camera_node gestartet")

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
