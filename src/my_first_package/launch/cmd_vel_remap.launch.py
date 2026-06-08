from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    cmd_vel_publisher_node = Node(
        package='my_first_package',
        executable='cmd_vel_publisher',
        output='screen',
        remappings=[
            ('/cmd_vel', '/turtle1/cmd_vel')
        ]
    )

    return LaunchDescription([
        cmd_vel_publisher_node
    ])
