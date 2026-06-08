import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    package_dir = get_package_share_directory('my_first_package')

    dist_turtle_action_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_dir, 'launch', 'dist_turtle_action.launch.py')
        )
    )

    tutlesim_and_teleop_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_dir, 'launch', 'turtlesim_and_teleop.launch.py')
        )
    )

    return LaunchDescription([
        dist_turtle_action_launch,
        tutlesim_and_teleop_launch
    ])
