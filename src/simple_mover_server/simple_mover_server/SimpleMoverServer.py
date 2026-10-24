import time
import rclpy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from interface_package .action import GoTo

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

        self._action_server = ActionServer(
            self,
            GoTo,
            'goto',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            handle_accepted_callback=self.handle_accepted_callback,
            cancel_callback=self.cancel_callback,
        )

        self.active_goal_handle = None

        print("Ende")

    #Bearbeitet neue Zielanfragen 
    def goal_callback(self, goal_request):

        #Wenn bereits Ziel aktiv --> altes Ziel abbrechen
        if (self.active_goal_handle is not None and self.active_goal_handle.is_active):

            #Ein vorheriges Ziel läuft noch. Es wird abgebrochen.')
            self.active_goal_handle.abort()

        return GoalResponse.ACCEPT

    # wird ausgeführt wenn Client abbruch schickt
    def cancel_callback(self, goal_handle):
        return CancelResponse.ACCEPT

    # Wird aufgerufen wenn Ziel akzeptiert wurde
    def handle_accepted_callback(self, goal_handle):

        #ruft execute_callback auf
        goal_handle.execute()


    def execute_callback(self, goal_handle):

        self.get_logger().info("Ausführung gestartet")

        #Setzt das aktive Ziel auf das aktuelle Ziel
        self.active_goal_handle = goal_handle

        #Feedback und Result
        feedback_msg = GoTo.Feedback()
        result = GoTo.Result()

        for i in range(10):

            if goal_handle.is_cancel_requested:

                goal_handle.canceled()
                self.get_logger().info('Ziel vom Client abgebrochen')
                result.success = False
                return result

            if not goal_handle.is_active:

                self.get_logger().info('Ziel wurde durch ein neues Ziel ersetzt (Preempted).')
                result.success = False
                return result

            #dummy feedback
            feedback_msg.distance = float(10 - i)
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Feedback: Noch {10 - i} Sekunden verbleibend.')
            print(i)
            time.sleep(1)

        if goal_handle.is_active:
            goal_handle.succeed()
            self.get_logger().info('Ziel erfolgreich abgeschlossen')
            result.success= True
            return result

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


