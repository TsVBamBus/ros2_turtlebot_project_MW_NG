import cv2
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


class ArucoNode(Node):
    def __init__(self):
        super().__init__("aruco_node")
        self.publisher = self.create_publisher(Bool, "/aruco/erkannt", 10)

        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
        parameter = cv2.aruco.DetectorParameters()
        self.detektor = cv2.aruco.ArucoDetector(dictionary, parameter)

        self.kamera = cv2.VideoCapture(0)
        self.timer = self.create_timer(0.2, self.pruefe_bild)

    def pruefe_bild(self):
        ok, bild = self.kamera.read()
        if not ok:
            self.get_logger().warn("Kein Bild bekommen")
            return

        grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
        ecken, ids, abgelehnt = self.detektor.detectMarkers(grau)

        nachricht = Bool()
        nachricht.data = ids is not None
        self.publisher.publish(nachricht)
        self.get_logger().info(f"Marker erkannt: {nachricht.data}")


def main():
    rclpy.init()
    node = ArucoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.kamera.release()
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == "__main__":
    main()
