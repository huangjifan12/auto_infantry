#!/usr/bin/env python3

from email.policy import default
import os

from launch.substitutions import EnvironmentVariable
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # lua config files
    lua_configuration_directory = os.path.join(
        get_package_share_directory("cartographer_test"), "config"
    )
    lua_configuration_name = "rplidar_2d.lua"

    # urdf model files
    urdf_model_name = "auto_infantry.urdf"
    urdf_model_path = os.path.join(
        get_package_share_directory("cartographer_test"), f"urdf/{urdf_model_name}"
    )

    # rviz config file
    rviz_config_dir = os.path.join(
        get_package_share_directory("cartographer_test"), "rviz", "sllidar_cartographer.rviz"
    )

    ld = LaunchDescription()

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        arguments=[urdf_model_path],
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        arguments=[urdf_model_path],
    )
    
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=['-d', rviz_config_dir],
        output="screen",
    )

    cartographer_node = Node(
        package="cartographer_ros",
        executable="cartographer_node",
        name="cartographer_node",
        arguments=[
            "-configuration_directory",
            lua_configuration_directory,
            "-configuration_basename",
            lua_configuration_name,
        ],
        remappings=[("scan", "scan")],
        output="screen",
    )

    occupancy_grid_node = Node(
        package="cartographer_ros",
        executable="occupancy_grid_node",
        name="occupancy_grid_node",
        arguments=["-resolution", "0.1"],
        output="screen",
    )

    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(rviz_node)
    ld.add_action(cartographer_node)
    ld.add_action(occupancy_grid_node)

    return ld
