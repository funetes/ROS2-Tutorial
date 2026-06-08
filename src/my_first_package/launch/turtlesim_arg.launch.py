from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    background_r = LaunchConfiguration('background_r')
    background_g = LaunchConfiguration('background_g')
    background_b = LaunchConfiguration('background_b')


    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        output='screen',
        parameters=[
            {
                'background_r': background_r,
                'background_g': background_g,
                'background_b': background_b
            },
        ]
    )

    dist_turtle_action_server = Node(
        package='my_first_package',
        executable='dist_turtle_action_server',
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'background_r',
            default_value='255',
            description='Turtlesim background red value'
        ),
        DeclareLaunchArgument(
            'background_g',
            default_value='255',
            description='Turtlesim background green value'
        ),
        DeclareLaunchArgument(
            'background_b',
            default_value='255',
            description='Turtlesim background blue value'
        ),
        turtlesim_node,
        dist_turtle_action_server
    ])


