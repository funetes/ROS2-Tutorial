import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class TurtlesimSubscriber(Node):
    def __init__(self):
        super().__init__("turtlesim_subscriber") # node name

        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

    def pose_callback(self, msg):
        self.get_logger().info(f'x={msg.x:.2f}, y={msg.y:.2f}, z={msg.theta:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = TurtlesimSubscriber();

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__name__':
    main();