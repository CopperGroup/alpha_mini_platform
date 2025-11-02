cmake_minimum_required(VERSION 4.0)
project(mystring_project VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if (MSVC)
    add_compile_options(/W4 /WX)
else()
    add_compile_options(-Wall -Wextra -pedantic -Werror=vla)
endif()

# --- Library ---
add_library(mystring STATIC
        src/mystring.cpp
)

target_include_directories(mystring PUBLIC
        ${PROJECT_SOURCE_DIR}/include
)

# --- Demo executable ---
add_executable(demo
        demo/main.cpp
)

target_link_libraries(demo PRIVATE mystring)