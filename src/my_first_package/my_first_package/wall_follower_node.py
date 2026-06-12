import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallFollowerNode(Node):
    def __init__(self):
        super().__init__('wall_follower_node')

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile_sensor_data
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.target_wall_distance = 0.65
        self.front_safe_distance = 0.65

        self.forward_speed = 0.08
        self.turn_speed = 0.45

        self.get_logger().info('wall_follower_node started')

    def scan_callback(self, msg: LaserScan):
        front = self.get_sector_min_distance(msg, -10.0, 10.0)
        front_right = self.get_sector_min_distance(msg, -55.0, -25.0)
        right = self.get_sector_min_distance(msg, -100.0, -80.0)

        cmd = Twist()

        if front < self.front_safe_distance:
            cmd.linear.x = 0.0
            cmd.angular.z = self.turn_speed
            state = 'TURN_LEFT_FRONT_OBSTACLE'
        elif right > self.target_wall_distance + 0.12:
            cmd.linear.x = self.forward_speed
            cmd.angular.z = -0.25
            state = 'TURN_RIGHT_FIND_WALL'
        elif right < self.target_wall_distance - 0.12:
            cmd.linear.x = self.forward_speed * 0.8
            cmd.angular.z = 0.25
            state = 'TURN_LEFT_TOO_CLOSE'
        else:
            cmd.linear.x = self.forward_speed
            cmd.angular.z = 0.0
            state = 'GO_STRAIGHT'
        
        self.cmd_pub.publish(cmd)

        self.get_logger().info(
            f'state={state}, front={front:.2f}, front_right={front_right:.2f}, right={right:.2f}'
        )

    def get_sector_min_distance(self, msg:LaserScan, start_deg:float, end_deg:float) -> float:
        start_rad = math.radians(start_deg)
        end_rad = math.radians(end_deg)

        start_index = int((start_rad - msg.angle_min) / msg.angle_increment)
        end_index = int((end_rad - msg.angle_min) / msg.angle_increment)

        start_index = max(0, min(start_index, len(msg.ranges) - 1))
        end_index = max(0, min(end_index, len(msg.ranges) - 1))

        if start_index > end_index:
            start_index, end_index = end_index, start_index
        
        sector_ranges = msg.ranges[start_index:end_index + 1]

        valid_ranges = []

        for distance in sector_ranges:
            if math.isfinite(distance):
                if msg.range_min < distance < msg.range_max:
                    valid_ranges.append(distance)
        
        if len(valid_ranges) == 0:
            return msg.range_max

        return min(valid_ranges)

def main(args=Node):
    rclpy.init()
    node = WallFollowerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
