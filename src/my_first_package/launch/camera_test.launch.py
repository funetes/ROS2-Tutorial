from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition

def generate_launch_description():
    use_camera = LaunchConfiguration('use_camera')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_camera',
            default_value='true',
            description='Whether to launch camera node'
        ),
        Node(
            package='my_first_package',
            executable='camera_node',
            output='screen',
            condition=IfCondition(use_camera)
        )
    ])

