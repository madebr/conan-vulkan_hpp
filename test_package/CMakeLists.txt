cmake_minimum_required(VERSION 2.8.12)
project(test_package CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(${PROJECT_NAME} OBJECT test_package.cpp)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})
