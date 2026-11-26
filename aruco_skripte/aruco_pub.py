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
        ergebnisse = self.erkennung.erkenne()  # ruft erkenne aus der logic auf
        if ergebnisse is None:  # bei read kam false zurück
            self.get_logger().warn("Kein Bild bekommen")
            return

        if len(ergebnisse) > 0:
            for m in ergebnisse:
                nachricht = Float32MultiArray()
                nachricht.data = [1.0, float(m["id"]), m["abstand"], m["winkel"]]
                self.pub_marker.publish(nachricht)#für jeden eintrag eine message
        else:
            nachricht = Float32MultiArray()
            nachricht.data = [0.0]  # Kein Marker erkannt = 0.0
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