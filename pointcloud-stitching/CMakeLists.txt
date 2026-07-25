# License: Apache 2.0. See LICENSE file in root directory.
# Copyright(c) 2026 Stan. All Rights Reserved.

cmake_minimum_required(VERSION 3.10)
project(stan-pointcloud-stitching)

include_directories(../include/h)
include_directories(../include/hpp)
include_directories(../imgui)

cmake_policy(SET CMP0072 NEW)
find_package(OpenGL REQUIRED)

add_executable(${PROJECT_NAME} stan-pointcloud-stitching.cpp )

target_link_libraries(${PROJECT_NAME} PRIVATE
  librealsense2.so
  OpenGL::GL
  OpenGL::GLU
  glfw
  imgui
)

install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
