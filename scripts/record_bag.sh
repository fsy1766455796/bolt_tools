#!/usr/bin/env bash
set -euo pipefail

timestamp="$(date +%Y_%m_%d-%H_%M_%S)"
output_dir="${1:-/home/oit/ros2_ws/bags/femto_bolt_${timestamp}}"

mkdir -p "$(dirname "$output_dir")"
echo "Recording rosbag to: $output_dir"

ros2 bag record \
  --output "$output_dir" \
  --compression-mode file \
  --compression-format zstd \
  /tf \
  /tf_static \
  /camera/color/image_raw \
  /camera/color/camera_info \
  /camera/depth/image_raw \
  /camera/depth/camera_info \
  /camera/depth_registered/points
