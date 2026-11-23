"""ROS-Schnittstelle: SystemNode (nur ROS, keine Logik)."""

from geometry_msgs.msg import Twist
from interface_package.msg import ArucoMarker
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

from system.sollwerte import Sollwerte
from system.system_logik import SystemLogik, Zustand


class SystemNode(Node):
    """Verteilt Sollwerte, setzt Zustände in Actions um, einziger Publisher auf /cmd_vel."""

    def __init__(self):
        super().__init__('system_node')
        self.logik = SystemLogik(rohrende_ids=(), id_hinten=0, id_vorne=0)   # TODO: echte IDs
        self.sollwerte = Sollwerte()

        # TODO: ActionClient(self, FahrenRohr, 'fahren_rohr') usw.
        self.client_fahren = None
        self.client_folgen = None
        self.client_wenden = None

        # TODO: create_publisher(...)
        self.pub_cmd_vel = None                 # Twist   -> /cmd_vel
        self.pub_soll_geschwindigkeit = None    # Float32 -> /soll/geschwindigkeit
        self.pub_soll_abstand = None            # Float32 -> /soll/abstand

        self.get_logger().info('system_node gestartet')

    def geschwindigkeit_callback(self, msg: Float32) -> None:
        """Gib die Geschwindigkeit an Sollwerte und publiziere sie bei Erfolg weiter."""
        raise NotImplementedError

    def abstand_callback(self, msg: Float32) -> None:
        """Gib den Abstand an Sollwerte und publiziere ihn bei Erfolg weiter."""
        raise NotImplementedError

    def aruco_callback(self, msg: ArucoMarker) -> None:
        """Gib die Marker an SystemLogik und setze einen neuen Zustand um."""
        raise NotImplementedError

    def fahren_cmd_callback(self, msg: Twist) -> None:
        """Leite den Befehl von fahren_rohr an /cmd_vel weiter, wenn er aktiv ist."""
        raise NotImplementedError

    def folgen_cmd_callback(self, msg: Twist) -> None:
        """Leite den Befehl von folgen an /cmd_vel weiter, wenn er aktiv ist."""
        raise NotImplementedError

    def wechsle_zu(self, zustand: Zustand) -> None:
        """Brich die laufende Action ab und starte die zum Zustand passende."""
        raise NotImplementedError

    def starte_action(self, client, goal, ist_wenden: bool = False) -> None:
        """Sende ein Goal asynchron; bei Wenden zusätzlich auf das Ergebnis warten."""
        raise NotImplementedError

    def wenden_fertig_callback(self, ergebnis) -> None:
        """Werte das Ergebnis der Wenden-Action aus und wechsle den Zustand."""
        raise NotImplementedError


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
