from interface_package.action import FahrenRohr, Folgen, Wenden
from interface_package.msg import ArucoMarker
import rclpy
from rclpy.action import CancelResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32

from fahren.fahren_logik import FahrenLogik


class FahrenNode(Node):
    
    def __init__(self):
        super().__init__('fahren_node')
        self.logik = FahrenLogik()

        # TODO: create_publisher(Twist, ...) -> wird von system_node abonniert
        self.pub_cmd = None

        # TODO: create_subscription(...)
        self.sub_soll_geschwindigkeit = None    # Float32
        self.sub_soll_abstand = None            # Float32
        self.sub_aruco = None                   # ArucoMarker
        self.sub_imu = None                     # Imu

        # TODO: ActionServer(self, FahrenRohr, ...), ActionServer(self, Folgen, ...),
        #       ActionServer(self, Wenden, ...)
        self.server_fahren = None
        self.server_folgen = None
        self.server_wenden = None

        self.get_logger().info('fahren_node gestartet')

    def soll_geschwindigkeit_callback(self, msg: Float32):
        return

    def soll_abstand_callback(self, msg: Float32):
        return

    def aruco_callback(self, msg: ArucoMarker):
        return

    def imu_callback(self, msg: Imu):
        return
    
    def fahren_execute(self, goal_handle: ServerGoalHandle):
        return

    def folgen_execute(self, goal_handle: ServerGoalHandle):
        return

    def wenden_execute(self, goal_handle: ServerGoalHandle):
        return

    def cancel_callback(self, goal_handle: ServerGoalHandle):
        return

    def sende_cmd(self, v: float, omega: float):
        return


def main():
    rclpy.init()
    node = FahrenNode()
    # TODO: MultiThreadedExecutor verwenden, damit Callbacks während der Actions laufen
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
