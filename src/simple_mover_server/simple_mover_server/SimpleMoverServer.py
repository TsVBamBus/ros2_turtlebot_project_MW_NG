import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

class GoToActionServer(Node):

    def __init__(self):
        super().__init__('goto_action_server')
        print('Hi from simple_mover_server.')
            #self._action_server = ActionServer(
            #self,
            #GoTo,
            #'goto',
            #self.execute_callback)

    #ef execute_callback(self):

def main():
    
    rclpy.init()

    goto_action_server = GoToActionServer()

    rclpy.spin(goto_action_server)


