from launch_ros.actions import Node 
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)


def generate_launch_description():
    ur_type = LaunchConfiguration("ur_type")
    robot_up = LaunchConfiguration("robot_ip")

    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    fake_sensor_commands = LaunchConfiguration("fake_sensor_commands")

    headless_mode = LaunchConfiguration("headless_mode")

    kinematics_parameters_file = LaunchConfiguration("kinematics_parameters_file")



    # Load description 
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [
                    FindPackageShare("robot_cell_control"),
                    "urdf",
                    "robot_cell_controlled.urdf.xacro",
                ]
            ),
            " ",
            "robot_ip:=",
            robot_ip,
            " ",
            "ur_type:=",
            ur_type,
            " ",
            "kinematics_parameters_file:=",
            kinematics_parameters_file,
            " ",
            "use_fake_hardware:=",
            use_fake_hardware,
            " ",
            "fake_sensor_commands:=",
            fake_sensor_commands,
            " ",
            "headless_mode:=",
            headless_mode,
        ]
    )
    # robot_description = {"robot_description": robot_description_content}
    robot_description = {
        "robot_descriptioin": ParameterValue(value=robot_description_content, value_type=str)
    }

    declared_arguments = []

    # UR specific arguments
    declared_arguments.append(
        DeclareLaunchArgument(
            "ur_type",
            description="Typo/series of used robot.",
            choices=[
                "ur3",
                "ur3e",
                "ur5",
                "ur5e",
                "ur10",
                "ur10e",
            ],
            default_value="ur10e",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_ip", 
            description="IP address by which the robot can be reached."
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "kinematics_parameters_file",
            default_value=PathJoinSubstitution(
                [
                    FindPackageShare("robot_cell_control"),
                    "config",
                    "my_robot_calibration.yaml"
                ]
            ),
            description="The calibration configuration of the actual robot used."
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="false",
            description="Start robot with mock hardware mirroring command to its states.",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "fake_sensor_commands",
            default_value="false",
            description="Enable move command interfaces for sensors used for simple simulations. \nUsed only if 'use_fake_hardware' parameter is true."
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "headless_mode",
            default_value="false",
            description="Enable headless mode for robot control",
        )
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        parameters = [
            {
                'zeros.robotiq_85_left_knuckle_joint': 0.632
            }
        ]
    )

    return LaunchDescription(
        declared_arguments
        + [
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="both",
                parameters=[robot_description]
            ),
        ]
        + [
            joint_state_publisher_node
        ]
    )