import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32MultiArray

from aruco_logic import ArucoErkennung


class ArucoNode(Node):
    def __init__(self):
        super().__init__("aruco_node")
      
        self.pub_marker = self.create_publisher(Float32MultiArray, "/aruco/marker", 2)

        self.erkennung = ArucoErkennung()
        self.timer = self.create_timer(1, self.pruefe_bild)

    def pruefe_bild(self):
        ergebnisse = self.erkennung.erkenne()
        if ergebnisse is None:
            self.get_logger().warn("Kein Bild bekommen")
            return

        nachricht = Float32MultiArray()
        if len(ergebnisse) > 0:
            daten = [1.0]  # True: Marker erkannt
            for m in ergebnisse:
                daten.extend([float(m["id"]), m["abstand"], m["winkel"]])
            nachricht.data = daten
        else:
            nachricht.data = [0.0]  # False: Kein Marker erkannt

        self.pub_marker.publish(nachricht)


        for m in ergebnisse:
            nachricht = Float32MultiArray()
            nachricht.data = [float(m["id"]), m["abstand"], m["winkel"]]
            self.pub_marker.publish(nachricht)


def main():
    rclpy.init()
    node = ArucoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.erkennung.schliessen()
    node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()


if __name__ == "__main__":
    main()