import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('my_first_package'),
        'config',
        'turtlesim_params.yaml'
    )

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        output='screen',
        parameters=[config]
    )

    return LaunchDescription([
        turtlesim_node
    ])
