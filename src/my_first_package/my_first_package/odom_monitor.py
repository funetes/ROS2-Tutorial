import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class OdomMonitor(Node):
    def __init__(self):
        super().__init__('odom_monitor_node')

        self.sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

    def odom_callback(self, msg: Odometry):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation

        yaw = math.atan2(
            2.0 * ((q.w * q.z) + (q.x * q.y)),
            1.0 - 2.0 * ((q.y * q.y) + (q.z * q.z))
        )

        linear_x = msg.twist.twist.linear.x
        angular_z = msg.twist.twist.angular.z

        self.get_logger().info(
            f'x={x:.3f}, y={y:.3f}, yaw={yaw:.3f}, '
            f'v={linear_x:.3f}, w={angular_z:.3f}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = OdomMonitor()
    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__ == "__main__":
    main()