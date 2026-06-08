from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        output='screen',
        parameters=[
            {'background_r': 255},
            {'background_g': 192},
            {'background_b': 203},
        ]
    )

    dist_turtle_action_server = Node(
        package='my_first_package',
        executable='dist_turtle_action_server',
        output='screen',
    )

    return LaunchDescription([
        turtlesim_node,
        dist_turtle_action_server
    ])
