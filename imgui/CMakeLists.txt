add_library(imgui SHARED)

file(GLOB IMGUI_SOURCES "*.cpp")
target_sources(imgui PRIVATE ${IMGUI_SOURCES})

install(TARGETS imgui LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})


