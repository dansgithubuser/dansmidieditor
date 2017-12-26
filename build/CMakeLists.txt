cmake_minimum_required(VERSION 3.2.3 FATAL_ERROR)

include("${CMAKE_CURRENT_SOURCE_DIR}/../deps/danssfml/CMakeHelpers.txt")

#=====include=====#
include_directories(
	"${CMAKE_CURRENT_SOURCE_DIR}/../deps/obvious/cpp"
	"${CMAKE_CURRENT_SOURCE_DIR}/../deps/danssfml"
)

#=====source=====#
set(src "${CMAKE_CURRENT_SOURCE_DIR}/../src/sfml.cpp")

#=====products=====#
set(output Sfml)
add_library(${output} MODULE ${src})
set_property(TARGET ${output} PROPERTY CXX_STANDARD 11)

#=====linking=====#
danssfml()
target_link_libraries(${output} sfml-system sfml-window sfml-graphics)
