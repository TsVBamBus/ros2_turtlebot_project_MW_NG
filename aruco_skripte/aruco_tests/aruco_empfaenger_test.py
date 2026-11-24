import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


class ArucoEmpfaenger(Node):
    def __init__(self):
        super().__init__("aruco_empfaenger")
        self.abo = self.create_subscription(
            Bool, "/aruco/erkannt", self.nachricht_erhalten, 10
        )

    def nachricht_erhalten(self, nachricht):
        if nachricht.data:
            self.get_logger().info("Marker wurde erkannt")
        else:
            self.get_logger().info("Kein Marker zu sehen")


def main():
    rclpy.init()
    node = ArucoEmpfaenger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == "__main__":
    main()