import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSReliabilityPolicy

class RobotDescriptionListener(Node):
    def __init__(self):
        super().__init__('robot_description_listener')

        qos_profile = QoSProfile(depth=1)
        qos_profile.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
        qos_profile.reliability = QoSReliabilityPolicy.RELIABLE

        self.subscription = self.create_subscription(
            String,
            '/robot_description',
            self.litener_callback,
            qos_profile
        )

        self.received_once = False

    def litener_callback(self, msg: String):
        if not self.received_once:
            self.get_logger().info('Received /robot_description')
            self.get_logger().info(f'URDF length: {len(msg.data)}')
            self.received_once = True

def main(args=None):
    rclpy.init(args=args)

    node = RobotDescriptionListener()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()



