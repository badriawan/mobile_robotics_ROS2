import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import  LaunchConfiguration


def generate_launch_description():

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']
    model_folder = 'turtlebot3_' + TURTLEBOT3_MODEL
    urdf_path = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'models',
        model_folder,
        'model.sdf'
    )

    x_pos = LaunchConfiguration('x_pos',default='0.0')
    y_pos = LaunchConfiguration('y_pos',default='0.0')
    yaw_rot = LaunchConfiguration('yaw_rot',default='0.0')
    robot_name = LaunchConfiguration('robot_name',default='waffle_pi')
    robot_ns = LaunchConfiguration('robot_ns',default='')


    robot_spawner = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', robot_name,
            '-file', urdf_path,
            '-x', x_pos,
            '-y', y_pos,
            '-z', '0.01',
            '-Y',yaw_rot,
            '-robot_namespace',robot_ns
        ],
        output='screen',
    )





    ld = LaunchDescription()

    # Add the commands to the launch description

    ld.add_action(robot_spawner)

    # Return the LaunchDescription
    return ld
