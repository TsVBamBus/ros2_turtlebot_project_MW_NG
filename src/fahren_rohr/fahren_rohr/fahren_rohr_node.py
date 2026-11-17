import rclpy
from rclpy.node import Node

class FahrenRohrNode(Node):

    def __init__(self):
        super().__init__("fahren_rohr_node")
        self.get_logger().info("fahren_rohr_node gestartet")

def main():
    rclpy.init()
    node = FahrenRohrNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
