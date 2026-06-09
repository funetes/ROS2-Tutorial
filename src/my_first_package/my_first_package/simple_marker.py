import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from rclpy.duration import Duration

class SimpleMarker(Node):
    def __init__(self):
        super().__init__('simple_marker_node')

        self.marker_pub = self.create_publisher(
            Marker,
            '/robot_marker',
            10
        )

        self.timer = self.create_timer(0.5, self.publish_marker)

    def publish_marker(self):
        marker = Marker()

        marker.header.frame_id = 'odom'
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = 'basic_shapes'
        marker.id = 0
        marker.type = Marker.ARROW
        marker.action = Marker.ADD

        marker.pose.position.x = 1.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.2

        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0

        marker.scale.x = 0.8
        marker.scale.y = 0.1
        marker.scale.z = 0.1

        marker.color.r = 1.0
        marker.color.g = 0.2
        marker.color.b = 0.2
        marker.color.a = 1.0

        marker.lifetime = Duration(seconds=0.0).to_msg()

        self.marker_pub.publish(marker)


def main(args=None):
    rclpy.init(args=args)
    node = SimpleMarker()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()