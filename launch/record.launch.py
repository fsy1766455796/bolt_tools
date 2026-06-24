from datetime import datetime

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    bag_root = LaunchConfiguration("bag_root")
    bag_name = LaunchConfiguration("bag_name")
    topics = LaunchConfiguration("topics")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "bag_root",
                default_value="/home/oit/ros2_ws/bags",
            ),
            DeclareLaunchArgument(
                "bag_name",
                default_value=f"femto_bolt_{datetime.now():%Y%m%d_%H%M%S}",
            ),
            DeclareLaunchArgument(
                "topics",
                default_value=(
                    "/tf /tf_static "
                    "/camera/color/image_raw /camera/color/camera_info "
                    "/camera/depth/image_raw /camera/depth/camera_info "
                    "/camera/depth/points"
                ),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [FindPackageShare("oit_rosbag"), "launch", "record_bag.launch.py"]
                    )
                ),
                launch_arguments={
                    "target": "custom",
                    "topics": topics,
                    "bag_root": bag_root,
                    "bag_name": bag_name,
                    "storage": "mcap",
                    "compression_mode": "none",
                    "storage_preset_profile": "none",
                }.items(),
            ),
        ]
    )
