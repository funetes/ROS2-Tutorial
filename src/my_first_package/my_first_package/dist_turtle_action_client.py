import rclpy as rp
from rclpy.action import ActionClient
from rclpy.node import Node

from my_first_package_msgs.action import DistTurtle

class DistTurtleCancelClient(Node):
    def __init__(self):
        super().__init__('dist_turtle_cancel_client')

        self._action_client = ActionClient(
            self,
            DistTurtle,
            'dist_turtle'
        )

        self.goal_handle = None
        self.timer = None

    def send_goal(self):
        goal_msg = DistTurtle.Goal()
        goal_msg.linear_x = 1.0
        goal_msg.angular_z = 0.0
        goal_msg.dist = 10.0

        # wait for server
        self._action_client.wait_for_server()

        self.get_logger().info('sending goal')

        self._send_goal_future = self._action_client.send_goal_async(
            goal=goal_msg,
            feedback_callback=self.feedback_callback # feedback callback
        )

        self._send_goal_future.add_done_callback(
            self.goal_response_callback
        )



    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        self.get_logger().info(
            f'Received feedback: remained_dist = {feedback.remained_dist}'
        )

    def goal_response_callback(self, future):
        self.goal_handle = future.result()

        # early return
        if not self.goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal_accepted')

        # call result as async
        self._get_result_future = self.goal_handle.get_result_async()
        self._get_result_future.add_done_callback(
            self.get_result_callback
        )

        self.timer = self.create_timer(2.0, self.cancel_goal)

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        self.get_logger().info(f'Action finished with status: {status}')
        self.get_logger().info(f'Result distance: {result.result_dist}')

        rp.shutdown()

    def cancel_goal(self):
        self.get_logger().info('sending cancel request')

        self.timer.cancel()

        self._cancel_future = self.goal_handle.cancel_goal_async()
        self._cancel_future.add_done_callback(
            self.cancel_done_callback
        )

    def cancel_done_callback(self, future):
        cancel_response = future.result()

        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info('Cancel request accepted')
        else:
            self.get_logger().info('Cancel request rejected')

def main(args=None):
    rp.init(args=args)
    dist_turtle_action_client = DistTurtleCancelClient()
    dist_turtle_action_client.send_goal()

    rp.spin(dist_turtle_action_client)

if __name__ == "__main__":
    main()
