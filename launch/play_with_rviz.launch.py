from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    bag_path = LaunchConfiguration("bag_path")
    rviz_config = LaunchConfiguration("rviz_config")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "bag_path",
                default_value="/home/oit/ros2_ws/bags/femto_bolt",
            ),
            DeclareLaunchArgument(
                "rviz_config",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("bolt_tools"), "rviz", "pointcloud.rviz"]
                ),
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
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["-d", rviz_config],
                output="screen",
            ),
        ]
    )
