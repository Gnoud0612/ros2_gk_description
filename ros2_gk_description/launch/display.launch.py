import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_name = 'ros2_gk_description'
    pkg_share = get_package_share_directory(pkg_name)

    # Đọc file URDF/Xacro
    urdf_file = os.path.join(pkg_share, 'urdf', 'ros2_gk.urdf.xacro')
    robot_description_config = xacro.process_file(urdf_file).toxml()

    return LaunchDescription([
        # Node phát sóng tọa độ robot
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_config}]
        ),
        # Node điều khiển khớp tay máy bằng thanh trượt
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
            parameters=[{'robot_description': robot_description_config}]
        ),
        # Mở RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        )
    ])
