# ros2_gk_description
# Tạo workspace và clone dự án
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Tải package về, đưa vào trong ros2_ws/src và biên dịch hệ thống
colcon build --packages-select ros2_gk_description
source install/setup.bash

# Khởi động mô phỏng gazebo/rviz
ros2 launch ros2_gk_description gazebo.launch.py

# Chạy SLAM (Lập bản đồ)
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true

# Điều khiển cánh tay robot
python3 src/ros2_gk_description/config/arm_teleop.py 

# Điều khiển robot di chuyển bằng bàn phím
ros2 run teleop_twist_keyboard teleop_twist_keyboard
