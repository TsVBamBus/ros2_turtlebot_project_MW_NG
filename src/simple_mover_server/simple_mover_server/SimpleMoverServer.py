import rclpy
from nav_msgs.msg import Odometry
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
        
        print("Ende")

    def odom_callback(self, msg):
        self.aktuelle_pos = [
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
        ]

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


