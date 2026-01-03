cmake_minimum_required(VERSION 3.15)
project(LucknowPathfinding)

set(CMAKE_CXX_STANDARD 17)
add_definitions(-DNOMINMAX)

# 1. Find the libosmium headers
find_path(OSMIUM_INCLUDE_DIR osmium/version.hpp)
if(NOT OSMIUM_INCLUDE_DIR)
    message(FATAL_ERROR "Could not find libosmium headers.")
endif()

# 2. Find ALL required dependencies
find_package(EXPAT REQUIRED)
find_package(ZLIB REQUIRED)
find_package(BZip2 REQUIRED) # Added this line
find_package(Threads REQUIRED)

add_executable(LucknowCore main.cpp)

# 3. Link everything together
target_include_directories(LucknowCore PRIVATE ${OSMIUM_INCLUDE_DIR})
target_link_libraries(LucknowCore PRIVATE 
    ${EXPAT_LIBRARIES} 
    ${ZLIB_LIBRARIES} 
    ${BZIP2_LIBRARIES} # Added this line
    ${CMAKE_THREAD_LIBS_INIT}
)