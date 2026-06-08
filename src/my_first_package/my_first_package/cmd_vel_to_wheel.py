import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray

class CmdVelToWheel(Node):
    def __init__(self):
        super().__init__('cmd_vel_to_wheel_node')

        self.declare_parameter('wheel_radius', 0.033) # r
        self.declare_parameter('wheel_separation', 0.30) # L

        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.wheel_separation = self.get_parameter('wheel_separation').value

        # create subsription

        self.sub_cmd_vel = self.create_subscription(Twist, '/turtle1/cmd_vel',self.cmd_vel_callback, 10)

        # create publish

        self.pub_wheel_velocity = self.create_publisher(Float32MultiArray, '/wheel_velocity', 10)

        self.get_logger().info('cmd_vel_to_whell node started.')
        self.get_logger().info(f'wheel_radius: {self.wheel_radius} m')
        self.get_logger().info(f'wheel_separation: {self.wheel_separation} m')

    def cmd_vel_callback(self, msg: Twist):
        linear_x = msg.linear.x
        angular_z  = msg.angular.z

        # linear velocity
        left_linear_velocity = linear_x - angular_z * self.wheel_separation / 2.0
        right_linear_velocity = linear_x + angular_z * self.wheel_separation / 2.0

        # angular velocity
        left_angular_velocity = left_linear_velocity / self.wheel_radius
        right_angular_velocity = right_linear_velocity / self.wheel_radius

        out = Float32MultiArray()

        out.data = [
            left_linear_velocity,
            right_linear_velocity,
            left_angular_velocity,
            right_angular_velocity
        ]

        self.pub_wheel_velocity.publish(out)

        self.get_logger().info(
            'cmd_vel '
            f'linear.x= {linear_x:.3f} m/s'
            f'angular.z= {angular_z:.3f} rad/s'
            f'left: {left_linear_velocity:.3f} m/s'
            f'right: {right_linear_velocity: .3f} m/s'
            f'left_w: {left_angular_velocity: .3f} rad/s'
            f'right_w: {right_angular_velocity: .3f} rad/s'
        )


def main(args=None):
    rclpy.init()
    node = CmdVelToWheel()

    rclpy.spin(node)

    node.destroy_node
    rclpy.shutdown()

if __name__ == "__main__":
    main();
