from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    bag_path = LaunchConfiguration("bag_path")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "bag_path",
                default_value="/home/oit/ros2_ws/bags/femto_bolt",
            ),
            ExecuteProcess(
                cmd=[
                    PathJoinSubstitution(
                        [FindPackageShare("bolt_tools"), "scripts", "play_bag.sh"]
                    ),
                    bag_path,
                ],
                output="screen",
            ),
        ]
    )
