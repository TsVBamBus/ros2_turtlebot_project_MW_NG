import rclpy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from rclpy.action import ActionServer
from rclpy.node import Node

class GoToActionServer(Node):

    def __init__(self):
        super().__init__('goto_action_server')
        print('Hi from simple_mover_server.')

        self.aktuelle_pos = [0.0, 0.0]
        print(self.aktuelle_pos)

        self.subscription = self.create_subscription(
            Odometry, 'odom', self.odom_callback, 10
        )

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        print("Ende")
        # Test-Aufruf: Sende einmalig ein Kommando beim Start
        self.publish_cmd_vel(0.0, 0.0)

    def odom_callback(self, msg):
        self.aktuelle_pos = [
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
        ]

    def publish_cmd_vel(self, linear_x, angular_z):
        twist = Twist()
        twist.linear.x = float(linear_x)
        twist.angular.z = float(angular_z)
        self.publisher_.publish(twist)

def main():
    
    rclpy.init()

    goto_action_server = GoToActionServer()

    try:
        rclpy.spin(goto_action_server)
    except KeyboardInterrupt:
        pass
    finally:
        goto_action_server.destroy_node()
        rclpy.shutdown()


