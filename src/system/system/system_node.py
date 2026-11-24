from geometry_msgs.msg import Twist
from interface_package.msg import ArucoMarker
import rclpy
from rclpy.node import Node
from rclpy.task import Future
from std_msgs.msg import Float32

from system.sollwerte import Sollwerte
from system.system_logik import SystemLogik
from system.zustand import Zustand


class SystemNode(Node):
    
    def __init__(self):
        super().__init__('system_node')
        # TODO: echte Marker-IDs eintragen
        self.logik = SystemLogik(id_rohr_hinten=0, id_rohr_vorne=0,
                                 id_robot_hinten=0, id_robot_vorne=0)
        self.sollwerte = Sollwerte()

        # TODO: ActionClient(self, FahrenRohr, ...), ActionClient(self, Folgen, ...),
        #       ActionClient(self, Wenden, ...)
        self.client_fahren = None
        self.client_folgen = None
        self.client_wenden = None
        self.aktives_ziel = None                # ClientGoalHandle der laufenden Action

        # TODO: create_publisher(...)
        self.pub_cmd_vel = None                 # Twist
        self.pub_soll_geschwindigkeit = None    # Float32
        self.pub_soll_abstand = None            # Float32

        # TODO: create_subscription(...)
        self.sub_geschwindigkeit = None         # Float32
        self.sub_abstand = None                 # Float32
        self.sub_aruco = None                   # ArucoMarker

        # TODO: create_timer(..., self.watchdog_callback)
        self.watchdog_timer = None

        self.get_logger().info('system_node gestartet')

    def geschwindigkeit_callback(self, msg: Float32):
        return

    def abstand_callback(self, msg: Float32):
       return

    def aruco_callback(self, msg: ArucoMarker):
        return

    def fahren_cmd_callback(self, msg: Twist):
        return

    def watchdog_callback(self):
        return

    def aktuelle_zeit(self):
        return

    def wechsle_zu(self, zustand: Zustand):
        return

    def starte_action(self, zustand: Zustand):
        return

    def fahren_fertig_callback(self, ergebnis: Future):
        return

    def wenden_fertig_callback(self, ergebnis: Future):
        return


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
