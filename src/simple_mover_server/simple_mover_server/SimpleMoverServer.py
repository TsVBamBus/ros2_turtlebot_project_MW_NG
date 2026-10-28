import time
import math
import rclpy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from simple_mover_server.Bahnberechnung import Bahnberechnung
from interface_package .action import GoTo

class GoToActionServer(Node):

    def __init__(self):
        super().__init__('goto_action_server')
        print('Hi from simple_mover_server.')

        #Initialisierung Bahnberechnung
        self.bahner = Bahnberechnung(
            toleranz=0.08,  # Toleranz für Zielereichung  0.08 = 10cm
            max_lin=0.22,   # max lineare Geschwindigkeit
            max_rot=1.0,    # max rotation Geschwindigkeit
            publisher=self.publish_cmd_vel,
        )

        print(self.bahner.aktuellePos())

        #Callback Group für ActionServer
        self.action_cb_group = ReentrantCallbackGroup()

        #Callback Group für OdomSubscriber
        self.odom_cb_group = MutuallyExclusiveCallbackGroup()

        self.subscription = self.create_subscription(
            Odometry, 'odom', self.odom_callback, 10, callback_group=self.odom_cb_group
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
            callback_group=self.action_cb_group,
        )

        self.active_goal_handle = None
        self.get_logger().info('Action Server ist bereit.')
        print("Ende")

    #Bearbeitet neue Zielanfragen 
    def goal_callback(self, goal_request):

        #Wenn bereits Ziel aktiv --> altes Ziel abbrechen
        if (self.active_goal_handle is not None and self.active_goal_handle.is_active):

            #Ein vorheriges Ziel läuft noch. Es wird abgebrochen
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

        # Setzt das aktive Ziel auf das aktuelle Ziel
        self.active_goal_handle = goal_handle

        # Zielkoordinaten aus dem Goal-Request
        ziel_x = goal_handle.request.target.x
        ziel_y = goal_handle.request.target.y
        self.bahner.setZiel(ziel_x, ziel_y)

        #Feedback und Result
        feedback_msg = GoTo.Feedback()
        result = GoTo.Result()

        while rclpy.ok():
            # 1. Prüfen, ob Client abgebrochen hat
            if goal_handle.is_cancel_requested:
                self.bahner.stopp()  # Roboter anhalten
                goal_handle.canceled()
                self.get_logger().info('Ziel vom Client abgebrochen.')
                result.success = False
                return result

            # 2. Prüfen, ob durch ein neueres Ziel verdrängt (preempted)
            if not goal_handle.is_active:
                self.bahner.stopp()
                self.get_logger().info('Ziel wurde präemptiert.')
                result.success = False
                return result

            # 3. Prüfen, ob das Ziel erreicht wurde
            if self.bahner.ziel_erreicht():
                self.bahner.stopp()
                goal_handle.succeed()
                self.get_logger().info('Ziel erfolgreich erreicht!')
                result.success = True
                return result

            # 4. Bahn berechnen und Fahrbefehl übergeben (wird via pubWeg automatisch an pub_cmd_vel gesendet)
            vel, rot = self.bahner.bahn()
            self.bahner.pubWeg((vel, rot))

            # 5. Live-Feedback senden (aktueller Abstand zum Ziel)
            feedback_msg.distance = float(self.bahner.abstand())
            goal_handle.publish_feedback(feedback_msg)

            time.sleep(0.05)  # 20 Hz Schleifenrate

        # Dummy Feedback Schleife
        """
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

        """

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        # 2. Orientierung (Quaternion) in Yaw-Winkel (theta) umrechnen
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        theta = math.atan2(siny_cosp, cosy_cosp)

        # 3. An die Bahnberechnung übergeben
        self.bahner.setAktuellePos(x, y, theta)

    def publish_cmd_vel(self, weg):
        linear_x, angular_z = weg
        twist = Twist()
        twist.linear.x = float(linear_x)
        twist.angular.z = float(angular_z)
        self.publisher_.publish(twist)

def main():
    
    rclpy.init()

    goto_action_server = GoToActionServer()

    executor = MultiThreadedExecutor()
    executor.add_node(goto_action_server)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        goto_action_server.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
