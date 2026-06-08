import rclpy
from rclpy.node import Node
from my_first_package_msgs.msg import EncoderTicks


class FakeEncoder(Node):
    def __init__(self):
        super().__init__('fake_encoder_node')

        self.pub = self.create_publisher(EncoderTicks, '/encoder_ticks', 10)

        self.left_ticks = 0
        self.right_ticks = 0

        self.declare_parameter('left_tick_step', 5)
        self.declare_parameter('right_tick_step', 5)
        self.declare_parameter('period', 0.05)

        self.left_tick_step = self.get_parameter('left_tick_step').value
        self.right_tick_step = self.get_parameter('right_tick_step').value
        self.period = self.get_parameter('period').value

        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('fake_encoder_node_started.')
    
    def timer_callback(self):
        self.left_ticks += int(self.left_tick_step)
        self.right_ticks += int(self.right_tick_step)

        msg = EncoderTicks()

        msg.left_ticks = self.left_ticks
        msg.right_ticks = self.right_ticks

        self.pub.publish(msg)

        self.get_logger().info(
            f'left_tisks: {self.left_ticks}, '
            f'right_ticks: {self.right_ticks}'
        )

def main(args=None):
    rclpy.init()
    node = FakeEncoder()

    rclpy.spin(node)
    node.destroy_node()

    rclpy.shutdown()

if __name__ == "__main__":
    main()
