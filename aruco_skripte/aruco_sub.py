import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray


class ArucoEmpfaenger(Node):
    def __init__(self):
        super().__init__("aruco_empfaenger")
        self.abo_marker = self.create_subscription(
            Float32MultiArray, "/aruco/marker", self.marker_erhalten, 10)

    def marker_erhalten(self, nachricht):
        daten = nachricht.data
        erkannt = bool(daten[0] == 1.0)

        if not erkannt:
            self.get_logger().info("Kein Marker erkannt")
            return

        self.get_logger().info("Marker erkannt:")
        for i in range(1, len(daten), 3):
            marker_id = int(daten[i])
            abstand = daten[i + 1]
            winkel = daten[i + 2]
            self.get_logger().info(
                f"  -> ID {marker_id}: Abstand {abstand * 100:.1f} cm, "
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