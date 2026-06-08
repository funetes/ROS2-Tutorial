import os
import glob

from setuptools import find_packages, setup

package_name = 'my_first_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
         glob.glob(os.path.join('launch', '*.launch.py'))
        ),
        ('share/' + package_name + '/config',
         glob.glob(os.path.join('config', '*.yaml'))
        )
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hwan',
    maintainer_email='hwan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'my_first_node = my_first_package.my_first_node:main',
            'my_subscriber = my_first_package.my_subscriber:main',
            'my_publisher = my_first_package.my_publisher:main',
            'turtle_cmd_and_pose = my_first_package.turtle_cmd_and_pose:main',
            'my_service_server = my_first_package.my_service_server:main',
            'dist_turtle_action_server = my_first_package.dist_turtle_action_server:main',
            'my_multi_thread = my_first_package.my_multi_thread:main',
            'phoato = my_first_package.dist_turtle_action_server_test:main',
            'dist_turtle_action_client = my_first_package.dist_turtle_action_client:main',
            'cmd_vel_publisher = my_first_package.cmd_vel_publisher:main',
            'camera_node = my_first_package.camera_node:main',
            'cmd_vel_to_wheel_node = my_first_package.cmd_vel_to_wheel:main',
            'fake_encoder_node = my_first_package.fake_encoder_node:main',
            'tick_to_distance = my_first_package.tick_to_distance:main'
        ],
    },
)
