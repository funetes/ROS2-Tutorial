import os
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_name = 'my_first_package'

    pkg_path = get_package_share_directory(package_name)
    xacro_file = os.path.join(pkg_path,'urdf','mobile_robot.urdf.xacro')

    robot_description = {
        'robot_description': Command(['xacro ' , xacro_file])
    }

    robot_state_publisher_node=Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description],
        output='screen'
    )

    joint_state_publisher_gui_node=Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    rviz_node=Node(
        package='rviz2',
        executable='rviz2',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])
