import rclpy
from rclpy.node import Node

class FolgenNode(Node):

    def __init__(self):
        super().__init__("folgen_node")
        self.get_logger().info("folgen_node gestartet")

def main():
    rclpy.init()
    node = FolgenNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
