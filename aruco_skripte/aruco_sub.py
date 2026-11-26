import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray


class ArucoEmpfaenger(Node):
    def __init__(self):
        super().__init__("aruco_empfaenger")
        self.abo_marker = self.create_subscription(
            Float32MultiArray, "/aruco/marker", self.marker_erhalten, 2)

    def marker_erhalten(self, nachricht):
        daten = nachricht.data
        erkannt = bool(daten[0] == 1.0)

        if not erkannt:
            self.get_logger().info("Kein Marker erkannt")
            return

        marker_id = int(daten[1])
        abstand = daten[2]
        winkel = daten[3]
        self.get_logger().info(
            f"Marker erkannt -> ID {marker_id}: Abstand {abstand * 100:.1f} cm, "
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