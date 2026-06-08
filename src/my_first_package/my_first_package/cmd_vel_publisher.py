import rclpy as rp
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelPuslisher(Node):
    
    def __init__(self):
        super().__init__('cmd_vel_publisher_node')

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(1.0, self.timer_callback)


    def timer_callback(self):
        msg = Twist()

        msg.linear.x = 1.0
        msg.angular.z = 0.5

        self.publisher.publish(msg)

        self.get_logger().info(
            'publish velocity command to /cmd_vel'
        )


def main(args=None):
    rp.init()

    cmd_vel_publisher = CmdVelPuslisher()

    rp.spin(cmd_vel_publisher)

    cmd_vel_publisher.destroy_node()
    rp.shutdown()


if __name__ == '__main__':
    main()
