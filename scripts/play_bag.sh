#!/usr/bin/env bash
set -euo pipefail

bag_path="${1:-/home/oit/ros2_ws/bags/femto_bolt}"

ros2 bag play "$bag_path" --clock
