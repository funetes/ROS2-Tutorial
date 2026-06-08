import math
import rclpy as rp
from rclpy.node import Node

from my_first_package_msgs.msg import EncoderTicks
from std_msgs.msg import Float64MultiArray

class TickToDistance(Node):
    def __init__(self):
        super().__init__('tick_to_distance_node')

        self.declare_parameter('wheel_radius', 0.033)
        self.declare_parameter('ticks_per_revolution', 2048)

        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.ticks_per_revolution = self.get_parameter('ticks_per_revolution').value

        self.distance_per_tick = 2 * math.pi / float(self.ticks_per_revolution)

        self.prev_left_ticks = None
        self.prev_right_ticks = None

        self.sub_encoder = self.create_subscription(
            EncoderTicks,
            '/encoder_ticks',
            self.encoder_callback,
            10
        )

        self.pub_encoder = self.create_publisher(Float64MultiArray, '/wheel_distance', 10)

        self.get_logger().info('tick_to_distance node started.')
        self.get_logger().info(f'wheel_radius: {self.wheel_radius} m')
        self.get_logger().info(f'ticks_per_revolution: {self.ticks_per_revolution}')
        self.get_logger().info(f'distance_per_tick: {self.distance_per_tick:.8f} m/tick')

    def encoder_callback(self, msg: EncoderTicks):
        left_ticks = msg.left_ticks
        right_ticks = msg.right_ticks

        if self.prev_left_ticks is None:
            self.prev_left_ticks = left_ticks
            self.prev_right_ticks = right_ticks
            self.get_logger().info('First encoder data received')
            return

        delta_left_ticks = left_ticks - self.prev_left_ticks
        delta_right_ticks = right_ticks - self.prev_right_ticks

        self.prev_left_ticks = left_ticks
        self.prev_right_ticks = right_ticks

        left_distance = delta_left_ticks * self.distance_per_tick
        right_distance = delta_right_ticks * self.distance_per_tick

        out = Float64MultiArray()

        out.data = [
            float(delta_left_ticks),
            float(delta_right_ticks),
            left_distance,
            right_distance
        ]

        self.pub_encoder.publish(out)

        self.get_logger().info(
            f'delta_ticks L={delta_left_ticks}, R={delta_right_ticks} | '
            f'distance L={left_distance:.5f} m, '
            f'R={right_distance:.5f} m'
        )

def main(args=None):
    rp.init()
    node = TickToDistance()
    rp.spin(node);

    node.destroy_node()

    rp.shutdown()

if __name__ == "__main__":
    main()
