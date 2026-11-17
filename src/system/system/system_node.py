import rclpy
from rclpy.node import Node

class SystemNode(Node):

    def __init__(self):
        super().__init__("system_node")
        self.get_logger().info("system_node gestartet")

def main():
    rclpy.init()
    node = SystemNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
