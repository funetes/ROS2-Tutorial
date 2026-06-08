import rclpy as rp
from rclpy.action import ActionServer, CancelResponse
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

from my_first_package_msgs.action import DistTurtle
import time
import math

from my_first_package.my_subscriber import TurtlesimSubscriber

from rcl_interfaces.msg import SetParametersResult

class TurtleSub_Action(TurtlesimSubscriber):
    # inject ac_server to use current_pose value
    def __init__(self, ac_server):
        super().__init__()
        # this, most important part.
        self.ac_server = ac_server

    def pose_callback(self, msg):
        self.ac_server.current_pose = msg #write

class DistTurtleServer(Node):
    def __init__(self):

        super().__init__("dist_turtle_action_server") # node name

        self.total_dist = 0
        self.is_fisrt_time = True

        self.current_pose = Pose() # inject pose interface
        self.previus_pose = Pose() # inject pose interface

        self.publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        self._action_server = ActionServer(
            self,
            DistTurtle,
            'dist_turtle',
            self.execute_callback,
            cancel_callback=self.cancel_callback
        )

        # add logger
        self.get_logger().info('Dist Turtle action server is started.')

        self.declare_parameter('quantile_time', 0.75)
        self.declare_parameter('almost_goal_time', 0.95)
        self.declare_parameter('goal_tolerance', 0.2)

        (a, b) = self.get_parameters([
            'quantile_time', 'almost_goal_time'
        ])

        self.goal_tolerance = self.get_parameter('goal_tolerance').value

        self.quantile_time = a.value
        self.almosts_time = b.value

        # add logger to parameters
        output_msg = 'quantile_time is ' + str(self.quantile_time) + ". "
        output_msg = output_msg + 'and almost_goal_time_is ' + str(self.almosts_time) + '.'

        self.get_logger().info(output_msg)

        self.add_on_set_parameters_callback(self.parameter_callback)

    def cancel_callback(self, goal_handle):
        self.get_logger().info('cancel request recieved')
        return CancelResponse.ACCEPT

    def parameter_callback(self, params):
        for param in params:
            print(param.name, "is changed to", param.value)

            if param.name == 'quantile_time':
                self.quantile_time = param.value
            if param.name == 'almost_goal_time':
                self.almosts_time = param.value
            if param.name == 'goal_tolerance':
                self.goal_tolerance = param.value

        print(
            'quantile_time and almost_goal_time is',
            self.quantile_time,
            self.almosts_time
        )
        return SetParametersResult(successful = True)

    def calc_diff_pose(self):
        if self.is_fisrt_time:
            self.previus_pose.x = self.current_pose.x
            self.previus_pose.y = self.current_pose.y
            self.is_fisrt_time = False

        diff_dist = math.sqrt(
            (self.current_pose.x - self.previus_pose.x) ** 2 +
            (self.current_pose.y - self.previus_pose.y) ** 2
            )
        self.previus_pose = self.current_pose

        return diff_dist


        # goal_handle is injected request interface
        # Request in goal_handle
        # float32 linear_x
        # float32 angular_z
        # float32 dist

    def execute_callback(self, goal_handle):
        # Inject Feedback Interface
        # float32 remained_dist
        feedback_msg = DistTurtle.Feedback()

        msg = Twist() # inject Twist interface
        msg.linear.x = goal_handle.request.linear_x
        msg.angular.z = goal_handle.request.angular_z
        # Result
        # float32 pos_x
        # float32 pos_y
        # float32 pos_theta
        # float32 result_dist
        result = DistTurtle.Result() # Inject Result Interface

        while True:
            if goal_handle.is_cancel_requested:
                self.get_logger().info('goal_ canceled')

                goal_handle.canceled()

                result.pos_x = 0.0
                result.pos_y = 0.0
                result.pos_theta = self.current_pose.theta
                result.result_dist = feedback_msg.remained_dist

                return result

            self.total_dist += self.calc_diff_pose()

            feedback_msg.remained_dist = (goal_handle.request.dist - self.total_dist)

            goal_handle.publish_feedback(feedback_msg)
            self.publisher.publish(msg)

            time.sleep(0.01)

            if feedback_msg.remained_dist < self.goal_tolerance:
                break

        goal_handle.succeed()

        result.pos_x = self.current_pose.x
        result.pos_y = self.current_pose.y
        result.pos_theta = self.current_pose.theta
        result.result_dist = self.total_dist

        self.total_dist = 0
        self.is_fisrt_time = True

        return result

def main(args=None):
    rp.init(args=args)

    executor = MultiThreadedExecutor()

    ac = DistTurtleServer()
    sub = TurtleSub_Action(ac_server=ac)

    executor.add_node(ac)
    executor.add_node(sub)

    try:
        executor.spin()

    finally:
        executor.shutdown()
        ac.destroy_node()
        sub.destroy_node()
        rp.shutdown()

    # instantitate
    # dist_turtle_action_server = DistTurtleServer()
    # execute server
    # rp.spin(dist_turtle_action_server)

    # dist_turtle_action_server.destroy_node()
    # rp.shutdown()

if __name__ == '__main__':
    main()
