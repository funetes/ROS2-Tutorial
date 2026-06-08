from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    namespace = LaunchConfiguration('namespace')

    return LaunchDescription([
        DeclareLaunchArgument(
            'namespace',
            default_value='robot1',
            description='Robot namespace'
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            namespace=namespace,
            output='screen'
        ),
        Node(
            package='my_first_package',
            executable='my_publisher',
            namespace=namespace,
            output='screen'
        )
    ])
