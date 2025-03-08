cmake_minimum_required(VERSION 3.15)
project(CThreads VERSION 1.0.0 LANGUAGES C)

# Set C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

# Add compiler-specific flags for MSVC
if(MSVC)
    # Add MSVC-specific compiler flags
    add_compile_options(/W4 /MP)
    
    # Disable specific warnings that might be too noisy
    add_compile_options(/wd4100 /wd4996)
    
    # Define _CRT_SECURE_NO_WARNINGS to avoid warnings about using standard C functions
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
endif()

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

# Source files
set(SOURCES
    src/main.c
    src/thread_basics.c
    src/mutex_demo.c
    src/condition_variables.c
    src/producer_consumer.c
    src/thread_specific_data.c
    src/thread_cancellation.c
    src/thread_pool.c
)

# Add the executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Windows-specific settings
if(WIN32)
    target_compile_definitions(${PROJECT_NAME} PRIVATE WIN32_LEAN_AND_MEAN)
    
    # Link against Windows libraries
    target_link_libraries(${PROJECT_NAME} PRIVATE winmm.lib)
endif()

# Set output directories
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)

# Add post-build message
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E echo "Build completed successfully!"
)

# Install target
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
)

# Create Visual Studio filters
if(MSVC)
    # Group source files in IDE
    source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCES})
endif() 