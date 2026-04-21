cmake_minimum_required(VERSION 3.8)
project(ros2_gk_description)

# Thiết lập cờ cảnh báo cho trình biên dịch C++ (chuẩn bị cho việc viết Node sau này)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Tìm kiếm các công cụ của ROS 2
find_package(ament_cmake REQUIRED)

# Install (cài đặt) các thư mục vào share/ để ROS 2 tìm thấy
install(
  DIRECTORY 
    urdf 
    meshes 
    launch
    config
    worlds
    rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
