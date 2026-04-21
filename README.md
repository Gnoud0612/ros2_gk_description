# ros2_gk_description
# Cập nhật danh sách gói của Ubuntu
sudo apt update

# Cài đặt các công cụ hiển thị và xử lý URDF/Xacro
sudo apt install -y ros-humble-xacro \
                    ros-humble-robot-state-publisher \
                    ros-humble-joint-state-publisher-gui \
                    ros-humble-rviz2

# Cài đặt môi trường Gazebo và các plugin cảm biến (Lidar, Camera, GPS)
sudo apt install -y ros-humble-gazebo-ros \
                    ros-humble-gazebo-plugins

# Cài đặt hệ thống điều khiển động cơ (Bánh xe vi sai & Tay máy)
sudo apt install -y ros-humble-ros2-control \
                    ros-humble-ros2-controllers \
                    ros-humble-gazebo-ros2-control \
                    ros-humble-teleop-twist-keyboard

# Cài đặt thuật toán Lập bản đồ (SLAM) và Tự hành (Navigation2)
sudo apt install -y ros-humble-slam-toolbox \
                    ros-humble-navigation2 \
                    ros-humble-nav2-bringup
# Tạo workspace và clone dự án
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Tải package ros2_gk_description về, đưa vào trong ros2_ws/src

# Lùi ra ngoài thư mục gốc và tiến hành biên dịch
cd ~/ros2_ws
colcon build --packages-select ros2_gk_description

# Nạp môi trường mỗi khi mở 1 terminal mới
source install/setup.bash

# Khởi động mô phỏng gazebo/rviz
ros2 launch ros2_gk_description gazebo.launch.py

# Chạy SLAM (Lập bản đồ)
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true

# Điều khiển cánh tay robot
python3 src/ros2_gk_description/config/arm_teleop.py 

# Điều khiển robot di chuyển bằng bàn phím
ros2 run teleop_twist_keyboard teleop_twist_keyboard
