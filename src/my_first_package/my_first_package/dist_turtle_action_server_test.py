import rclpy as rp
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from my_first_package_msgs.action import DistTurtle
from my_first_package.my_subscriber import TurtlesimSubscriber
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

import time
import math

class TurtleSub_Action_Test(TurtlesimSubscriber):
    def __init__(self, ac_server):  # inject action server for write current pose from pose subscribe node
        super().__init__()
        self.ac_server = ac_server

    def pose_callback(self, msg):
        self.ac_server.current_pose = msg


class DistTurtleActionServerTest(Node):
    def __init__(self):
        super().__init__('SuperPower') # node name

        self.total_dist = 0
        self.is_first_time = True
        self.current_pose = Pose()
        self.previus_pose = Pose()

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self._action_server = ActionServer(
            self,
            DistTurtle,
            'SuperPowerActionServer', #action name
            self.callback
        )
    def calc_diff_pose(self):
        if self.is_first_time:
            self.previus_pose.x = self.current_pose.x
            self.previus_pose.y = self.current_pose.y
            self.is_first_time = False

        diff_dist = math.sqrt(
            (self.current_pose.x - self.previus_pose.x) ** 2 +
            (self.current_pose.y - self.previus_pose.y) ** 2
        )

        self.previus_pose = self.current_pose

        return diff_dist

    def callback(self, goal_handle):
        feedback_msg = DistTurtle.Feedback()

        # save data from request
        msg = Twist()
        msg.linear.x = goal_handle.request.linear_x
        msg.angular.z = goal_handle.request.angular_z

        while True:
            self.total_dist += self.calc_diff_pose()

            # save feedback data
            feedback_msg.remained_dist = (goal_handle.request.dist - self.total_dist)

            # publish feedback data
            goal_handle.publish_feedback(feedback_msg)

            # publish cmd_vel
            self.publisher.publish(msg)

            time.sleep(0.1)

            if feedback_msg.remained_dist < 0.2:
                break

        goal_handle.succeed()

        result = DistTurtle.Result()
        result.pos_x = self.current_pose.x
        result.pos_y = self.current_pose.y
        result.pos_theta = self.current_pose.theta
        result.result_dist = self.total_dist

        self.total_dist = 0
        self.is_first_time = False
        return result


def main():
    rp.init()
    executor = MultiThreadedExecutor()

    dist_turtle_action_server_test = DistTurtleActionServerTest()
    sub = TurtleSub_Action_Test(dist_turtle_action_server_test)

    executor.add_node(dist_turtle_action_server_test)
    executor.add_node(sub)

    try:
        executor.spin()

    finally:
        executor.shutdown()
        dist_turtle_action_server_test.destroy_node()
        sub.destroy_node()
        rp.shutdown()
    # rp.spin(dist_turtle_action_server_test)
    # rp.shutdown()

if __name__ == "__main__":
    main()

