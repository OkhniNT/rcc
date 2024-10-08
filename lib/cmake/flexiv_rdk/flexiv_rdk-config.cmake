include(CMakeFindDependencyMacro)

# Find dependency
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_dependency(Threads REQUIRED)

# Add targets file
include("${CMAKE_CURRENT_LIST_DIR}/flexiv_rdk-targets.cmake")
