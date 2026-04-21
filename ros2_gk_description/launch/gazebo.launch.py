import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_name = 'ros2_gk_description'
    pkg_path = os.path.join(get_package_share_directory(package_name))
    xacro_file = os.path.join(pkg_path, 'urdf', 'ros2_gk.urdf.xacro')

    doc = xacro.process_file(xacro_file)
    robot_description = {'robot_description': doc.toxml()}

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # ĐỊNH NGHĨA ĐƯỜNG DẪN TỚI FILE WORLD
    world_file = os.path.join(pkg_path, 'worlds', 'test_room.world')

    # KHỞI ĐỘNG GAZEBO KÈM THEO WORLD
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'world': world_file}.items()
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'ros2_gk_robot', '-z', '0.5'],
        output='screen'
    )

    delayed_spawn = TimerAction(period=3.0, actions=[spawn_entity])

    # Gọi các bộ điều khiển cánh tay (Đợi 6s cho xe rớt xuống sàn xong mới bật)
    load_joint_state_broadcaster = TimerAction(
        period=6.0,
        actions=[Node(package="controller_manager", executable="spawner", arguments=["joint_state_broadcaster"])]
    )

    load_arm_controller = TimerAction(
        period=7.0,
        actions=[Node(package="controller_manager", executable="spawner", arguments=["arm_controller"])]
    )

    # --- ĐOẠN CODE RVIZ 
    rviz_config_path = os.path.join(pkg_path, 'rviz', 'slam_config.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen'
    )
    
    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        delayed_spawn,
        load_joint_state_broadcaster, # Bật báo cáo trạng thái khớp
        load_arm_controller,          # Bật điều khiển cánh tay
        rviz_node
    ])
