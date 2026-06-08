cmake_minimum_required(VERSION 3.8)
project(my_cpp_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(my_first_package_msgs REQUIRED)
find_package(rclcpp_action REQUIRED)

add_executable(simple_publisher src/simple_publisher.cpp)
ament_target_dependencies(simple_publisher rclcpp std_msgs)

add_executable(simple_subscriber src/simple_subscriber.cpp)
ament_target_dependencies(simple_subscriber rclcpp std_msgs)

add_executable(temperature_publisher src/temperature_publisher.cpp)
ament_target_dependencies(temperature_publisher rclcpp std_msgs)

add_executable(temperature_subscriber src/temperature_subscriber.cpp)
ament_target_dependencies(temperature_subscriber rclcpp std_msgs)

add_executable(math_server src/math_server.cpp)
ament_target_dependencies(math_server rclcpp std_msgs my_first_package_msgs)

add_executable(math_client src/math_client.cpp)
ament_target_dependencies(math_client rclcpp std_msgs my_first_package_msgs)

add_executable(move_distance_server src/move_distance_server.cpp)
ament_target_dependencies(move_distance_server rclcpp std_msgs my_first_package_msgs rclcpp_action)

add_executable(move_distance_client src/move_distance_client.cpp)
ament_target_dependencies(move_distance_client rclcpp std_msgs my_first_package_msgs rclcpp_action)

add_executable(mobile_base_controller src/mobile_base_controller.cpp)
ament_target_dependencies(mobile_base_controller rclcpp)

add_executable(patrol_node src/patrol_node.cpp)
ament_target_dependencies(patrol_node rclcpp)

add_executable(emergency_stop_server src/emergency_stop_server.cpp)
ament_target_dependencies(emergency_stop_server rclcpp std_msgs my_first_package_msgs)

add_executable(emergency_stop_client src/emergency_stop_client.cpp)
ament_target_dependencies(emergency_stop_client rclcpp std_msgs my_first_package_msgs)

install(TARGETS
  simple_publisher
  simple_subscriber
  temperature_publisher
  temperature_subscriber
  math_server
  math_client
  move_distance_server
  move_distance_client
  mobile_base_controller
  patrol_node
  emergency_stop_server
  emergency_stop_client
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
