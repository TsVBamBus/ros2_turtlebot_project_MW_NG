import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32MultiArray


class ArucoEmpfaenger(Node):
    def __init__(self):
        super().__init__("aruco_empfaenger")
        self.abo_erkannt = self.create_subscription(
            Bool, "/aruco/erkannt", self.erkannt_erhalten, 10)
        self.abo_marker = self.create_subscription(
            Float32MultiArray, "/aruco/marker", self.marker_erhalten, 10)

    def erkannt_erhalten(self, nachricht):
        if nachricht.data:
            self.get_logger().info("Marker erkannt")
        else:
            self.get_logger().info("Kein Marker erkannt")

    def marker_erhalten(self, nachricht):
        marker_id = int(nachricht.data[0])
        abstand = nachricht.data[1]
        winkel = nachricht.data[2]
        self.get_logger().info(
            f"ID {marker_id}: Abstand {abstand * 100:.1f} cm, "
            f"Winkel {winkel:.1f} Grad")


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