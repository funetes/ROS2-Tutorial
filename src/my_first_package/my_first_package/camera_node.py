import rclpy as rp
from rclpy.node import Node


class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')

        self.get_logger().info('camera_node has been started')
        self.get_logger().info('this is a dummy camera node for launch condition test.')

        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        self.count += 1
        self.get_logger().info(f'Dummy camera node is running... count: {self.count}')

def main(args=None):
    rp.init(args=args)

    node = CameraNode()

    try:
        rp.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('camera_node stopped by user.')
    finally:
        node.destroy_node()
        rp.shutdown()

if __name__ == '__main__':
    main()

