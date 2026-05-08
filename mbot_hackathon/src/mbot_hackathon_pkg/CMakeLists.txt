cmake_minimum_required(VERSION 3.8)
project(mbot_hackathon_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate custom messages and services
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Command.msg"
  "srv/GetCommands.srv"
  "srv/TextToSpeech.srv"
)

# Install the nodes
install(PROGRAMS
  nodes/agent_node.py
  nodes/manager_node.py
  nodes/test_speech_to_text_node.py
  nodes/test_text_to_speech_node.py
  nodes/text_to_speech_node.py
  nodes/speech_to_text_node.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
