

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.actions import TimerAction

def generate_launch_description():
    # Create a new LaunchDescription
    ld = LaunchDescription()

    ##### Starting the turtlesim_node
    # This node starts the turtlesim simulation.
    turtlesim1 = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim1',
    )
    kill_first = ExecuteProcess(
        cmd=['ros2', 'service', 'call', '/kill', 'turtlesim/srv/Kill', "\"{name: 'turtle1'}\"",],
        name='kill_turtle1',
        shell=True
    )


    ##### Spawning the first turtle
    # This command calls the /spawn service to create a new turtle at coordinates (3, 1) after a delay of 2 seconds.
    spawn_turtle_1 = ExecuteProcess(
        cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', "\"{x: 3.0, y: 1.0, theta: 1.57, name: 'turtle1'}\"",],
        name='spawn_turtle1',
        shell=True
    )

    spawn_turtle1_delayed = TimerAction(
            period=2.0,
            actions=[spawn_turtle_1],
        )

    spawn_turtle2_delayed = TimerAction(
            period=2.0,
            actions=[spawn_turtle_1],
        )


    ##### Spawning the second turtle
    # This command calls the /spawn service to create a second turtle at coordinates (2, 1).
    spawn_turtle_2 = ExecuteProcess(
        cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', "\"{x: 4.0, y: 1.0, theta: 1.57, name: 'turtle2'}\"",],
        name='spawn_turtle2',
        shell=True
    )


    turtle1_controller = Node(
        package='drive_turtle',
        executable='test_run',
        name='turtle1_controller',
        parameters=[
            {'cmd_vel_topic': '/turtle1/cmd_vel'},
            {'linear_velocity': 2.5}
        ]
    )

    turtle2_controller = Node(
        package='drive_turtle',
        executable='test_run',
        name='turtle2_controller',
        parameters=[
            {'cmd_vel_topic': '/turtle2/cmd_vel'},
            {'linear_velocity': 1.0}
        ]
    )
    # Add the nodes and actions to the LaunchDescription
    ld.add_action(turtlesim1)
    ld.add_action(kill_first)
    ld.add_action(spawn_turtle1_delayed)
    ld.add_action(spawn_turtle_2)
    ld.add_action(turtle1_controller)
    ld.add_action(turtle2_controller)

    # Return the LaunchDescription
    return ld
