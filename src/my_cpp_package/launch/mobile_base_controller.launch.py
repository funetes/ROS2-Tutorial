import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('my_cpp_package'),
        'config',
        'mobile_base_controller.yaml'
    )

    return LaunchDescription([
        Node(
            package='my_cpp_package',
            executable='mobile_base_controller',
            name='mobile_base_controller',
            output='screen',
            parameters=[config]
        )
    ])
