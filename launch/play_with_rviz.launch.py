import os
from datetime import datetime

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def _bag_size(path):
    total = 0
    for root, _, files in os.walk(path):
        for filename in files:
            try:
                total += os.path.getsize(os.path.join(root, filename))
            except OSError:
                pass
    return total


def _format_size(size):
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if size < 1024 or unit == "TiB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} {unit}"
        size /= 1024


def _discover_bags(bag_root):
    if not os.path.isdir(bag_root):
        return []

    bags = []
    for name in os.listdir(bag_root):
        path = os.path.join(bag_root, name)
        if not os.path.isdir(path):
            continue
        try:
            files = os.listdir(path)
        except OSError:
            continue
        has_data = any(filename.endswith((".mcap", ".db3")) for filename in files)
        if not has_data:
            continue
        mtime = os.path.getmtime(path)
        bags.append((mtime, path))

    bags.sort(key=lambda item: item[0], reverse=True)
    return bags


def _select_bag_path(context, *args, **kwargs):
    bag_path = LaunchConfiguration("bag_path").perform(context).strip()
    bag_root = LaunchConfiguration("bag_root").perform(context).strip()
    rviz_config = LaunchConfiguration("rviz_config").perform(context)

    if not bag_path:
        bags = _discover_bags(bag_root)
        if not bags:
            raise RuntimeError(f"No rosbag directories with .mcap or .db3 files found in {bag_root}")

        print("\nSelect rosbag to play:")
        for index, (mtime, path) in enumerate(bags):
            timestamp = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{index}] {os.path.basename(path)}  {timestamp}  {_format_size(_bag_size(path))}")

        selection = input("rosbag number [0]: " ).strip()
        if not selection:
            selection = "0"
        try:
            index = int(selection)
        except ValueError as exc:
            raise RuntimeError(f"Invalid rosbag number: {selection}") from exc
        if index < 0 or index >= len(bags):
            raise RuntimeError(f"Rosbag number out of range: {index}")
        bag_path = bags[index][1]

    print(f"Playing rosbag: {bag_path}")
    return [
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


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "bag_root",
                default_value="/home/oit/ros2_ws/bags",
            ),
            DeclareLaunchArgument(
                "bag_path",
                default_value="",
            ),
            DeclareLaunchArgument(
                "rviz_config",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("bolt_tools"), "rviz", "pointcloud.rviz"]
                ),
            ),
            OpaqueFunction(function=_select_bag_path),
        ]
    )
