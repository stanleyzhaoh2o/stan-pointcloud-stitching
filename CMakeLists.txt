cmake_minimum_required(VERSION 3.10)
project(stan-pc-stitching C CXX)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Release)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Release)

add_subdirectory(include)
add_subdirectory(imgui)
add_subdirectory(pointcloud-stitching)
